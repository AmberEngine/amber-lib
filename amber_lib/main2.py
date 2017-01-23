from datetime import datetime
import base64
import copy
import hashlib
import json
import re
import warnings
import functools

import requests

from urllib.parse import quote, urlparse


HTTP_ERRORS = {}

def http_error(number):
    def inner(class_):
        HTTP_ERRORS[number] = class_
        class_.status_code = number
        return class_
    return inner


class HTTPError(Exception):
    def __init__(self, *args, **kwargs):

        super(HTTPError, self).__init__(*args, **kwargs)


@http_error(400)
class BadRequest(HTTPError):
    pass


@http_error(401)
class Unauthorized(HTTPError):
    pass


@http_error(403)
class Forbidden(HTTPError):
    pass


@http_error(404)
class NotFound(HTTPError):
    pass


@http_error(405)
class MethodNotAllowed(HTTPError):
    pass


@http_error(406)
class NotAcceptable(HTTPError):
    pass


@http_error(410)
class Gone(HTTPError):
    pass


@http_error(415)
class UnsupportedMediaType(HTTPError):
    pass


@http_error(418)
class ImaTeapot(HTTPError):
    pass


@http_error(419)
class AuthenticationTimeout(HTTPError):
    pass


@http_error(500)
class ServerError(HTTPError):
    pass


def create_url(context, endpoint, **uri_args):
    """ Create a full URL using the context settings, the desired endpoint,
    and any option URI (keyword) arguments.
    """
    host = context.host.rstrip('/')
    url = '%s:%s%s' % (host, context.port, endpoint)

    if not context.port or context.port == '80':
        url = '%s%s' % (host, endpoint)

    if len(uri_args) > 0:
        url += '?'
        query_params = []
        for key in sorted(uri_args.keys()):
            val = str(uri_args[key])
            val = quote(val, safe='')
            key = quote(key, safe='')
            query_params.append('%s=%s' % (key, val))

        url += '&'.join(query_params)

    # Returns a validated URL
    return urlparse(url).geturl()


def send(method, ctx, endpoint, json_data=None, **uri_params):
    """ Create and execute an HTTP request at the specified endpoint,
    with the described method, context, and request data.
    """
    method = method.lower()
    if method not in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
        raise AttributeError('Bad HTTP method provided: %s' % method)

    def dump(data):
        return json.dumps(data, sort_keys=True, separators=(',', ':'))

    url = create_url(ctx, endpoint, **uri_params)
    if json_data:
        payload = dump(json_data)
    else:
        payload = '{}'
    current_timestamp = datetime.isoformat(datetime.utcnow())


    auth_string = ''

    # Standard headers that are present for each HTTP request.
    headers = {
            'Accept': 'application/hal+json',
            'Content-Type': 'application/json',
            'Public-Key': ctx.public if ctx.public else '',
            'Timestamp': current_timestamp,
            'URL': url
            }

    if ctx.token:
        # If a JWT token is available, use in-place of signature.
        auth_string = ctx.token
    else:
        # Create a signiture using the request's headers and the payload
        # data.
        # Encode/decode is required for the hashing/encrypting functions.
        sig = '%s%s%s' % (dump(headers), payload, ctx.private)
        sig = base64.b64encode(
                hashlib.sha256(sig.encode('utf-8')).hexdigest().encode('utf-8')
                ).decode('ascii')
        auth_string = sig

    headers['Authorization'] = 'Bearer %s' % auth_string

    r = None
    retry_on = [408, 419, 500, 502, 504]
    attempts = 0
    while attempts < ctx.request_attempts:
        r = getattr(requests, method)(url, data=payload, headers=headers)
        status = r.status_code
        if status == 200:
            try:
                return r.json()
            except ValueError:
                return {}
        elif status == 440 and ctx.on_token_refresh:
            claims = ctx.token.split('.')[1]
            if 4 - len(claims) % 4 > 0:
                claims += '=' * (4 - len(claims) % 4)
            ctx.token = ''
            ctx.token = ctx.create_token(public=sub)
            ctx.on_token_refresh(ctx.token)
            return send(method, ctx, endpoint, json_data, **uri_params)
        elif status in retry_on:
            attempts += 1
        else:
            break
    error = {}
    try:
        error = r.json()
    except ValueError:
        pass # response did not include any JSON

    status_code = r.status_code
    if status_code in HTTP_ERRORS:
        raise HTTP_ERRORS[status_code](method, url)
    else:
        raise Exception(method, url)


class Context(object):
    """ Context contains contextual data for generating data requests to the
    Conn. Used for determining which Conn is being hit, contains authentication
    information, and optional parameters.
    """
    host = ''
    port = ''
    private = ''
    public = ''
    request_attempts = 3
    token = ''
    on_token_refresh = None

    def __init__(self, **kwargs):
        """ Create a new instance of Context, using keyword arguments to
        override class defaults.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                if isinstance(value, str):
                    value = value.strip()
                setattr(self, key, value)

    def create_token(self, public='', use_token=False):
        if not public:
            public = self.public
        returned_dict = send(
                POST,
                self,
                '/tokens',
                {'public': public},
                )
        key = returned_dict['key']

        if use_token:
            self.token = key
        return key


class Resource(object):
    def __init__(self):
        super(Resource, self).__init__()

        self._affordances = {}

    def _add_affordance(self, name, fn):
        self._affordances[name] = fn

    def __getattr__(self, key):
        if key in self._affordances:
            return self._affordances[key]

        return super(Resource, self).__getattr__(key)


class ResourceInstance(object):
    """ A ResourceInstance instance is made up by an internal state, any embedded
    external resources, and any affordances for the current resource.
    The state can be accessed via dictionary-notation (eg: res['id']), while
    the affordance functions can be accessed like normal methods.

    Note that `unsaved_state_keys` is not operational.
    Note that there may be method naming collisions (like 'update').
    Note that inserting the current state of the resource into outbound
    affordance requests has not been implemented yet (so no "update" or "create"
    functionallity).
    """
    def __init__(self):
        super(ResourceInstance, self).__init__()

        self.state = {}
        self.affordances = {}
        self._unsaved_keys = set()

        self.embedded = {}


    def _add_affordance(self, name, fn):
        self.affordances[name] = fn

    def __getattr__(self, key):
        if key in self.affordances:
            return self.affordances[key]
        return self.__dict__[key]

    def _from_response(self, ctx, dict_):
        for key, value in dict_.items():
            if key == '_embedded':
                for resName, resListing in value.items():
                    for embeddedState in resListing:
                        inst = ResourceInstance()
                        inst._from_response(ctx, embeddedState)

                        if resName not in self.embedded:
                            self.embedded[resName] = []
                        self.embedded[resName].append(inst)
            elif key == '_links':
                if isinstance(value, dict):
                    value = [val for val in value.values()]

                for aff in value:
                    method = aff.get('method', 'get')
                    templated = aff.get('templated', False)
                    name = aff.get('name', '')
                    href = aff.get('href', '')
                    self._add_affordance(name, functools.partial(create_affordance(ctx, method, href, templated), body=self.state))
            else:
                self.state[key] = value

    def __delitem__(self, key):
        if key not in self.state:
            raise KeyError("'%s'" % key)

        self.unsaved_state_keys.remove(key)
        del self.state[key]

    def __repr__(self):
        return "<%s '%s' at %s>" % (
            'empty' if not self.state else 'populated',
            self.__class__.__name__,
            hex(id(self))
        )

    def __str__(self):
        """ Printing a ResourceInstance instance will result in printing *just* the current
        state of the resource.
        Embedded resources and afforances are not currently included.
        """
        return json.dumps(self.state, sort_keys=True, indent=4)


def create_affordance(ctx, method, href, templated):
    """ Create and return a new affordance function, which will be based off
    the context, method,  href, and templated arguments.

    If the href is templated, it's position arguments become *required*.
    In addition, if kwargs are provided that do not match any of the optional
    URI query param keys an error is outputted. (Note that JSON params still
    need to be supported).
    """
    posArgRegEx = re.compile('{([a-zA-Z0-9_]+)}') # Example match: /component/{comp_name}
    kwArgRegEx = re.compile('{[?&]([a-zA-Z0-9_,]+)}') # Example match: /listing{?limit,offset,sort_by}

    def fn(*args, **kwargs):
        """ This is a dynamically generated function, which utilizes the
        method type, href url, templated boolean, and Context instance from its
        parent scope.
        This function will result in a HTTP call to the Conn.
        Postional args replace tempalted positional URI args, while kwargs
        replace option URI query parameters (and eventually JSON body params).
        """

        body = {}
        if 'body' in kwargs:
            body = kwargs['body']
            del kwargs['body']

        if not templated:
            # href is not tempalted, so we can just do the HTTP call.
            for key, val in kwargs.items():
                if key not in kwArgMatches:
                    # Output to StdErr whenever a kwarg does not match any of
                    # the specified URI query param keys.
                    warnings.warn("function argument '%s' not a valid URI query param" % key, UserWarning)
            dict_ = send(method, ctx, href, json_data=body, **kwargs)
            inst = ResourceInstance()
            inst._from_response(ctx, dict_)

            return inst

        # Convert args and kwargs (both keys and vals) to be strings.
        args = [str(arg) for arg in args]
        kwargs = {str(k): str(v) for k, v in kwargs.items()}

        posArgMatches = posArgRegEx.findall(href)
        kwArgMatches = []

        kwMatch = kwArgRegEx.findall(href)
        if len(kwMatch) == 1:
            kwArgMatches = kwMatch[0].split(",")

        # Ensure that the number of provided args matches the required number
        # of positional arguments as determined from the tempalted href.
        if len(args) != len(posArgMatches):
            diff = len(args) - len(posArgMatches)
            if diff > 0:
                raise TypeError("Too many positional arguments included: '%s'" % ", ".join(args[:diff]))
            diff *= -1
            raise TypeError("Missing positional arguments: '%s'" % ", ".join(posArgMatches[:diff]))


        if kwargs:
            for key, val in kwargs.items():
                if key not in kwArgMatches:
                    # Output to StdErr whenever a kwarg does not match any of
                    # the specified URI query param keys.
                    warnings.warn("function argument '%s' not a valid URI query param" % key, UserWarning)

        non_templated_href = href

        # Replace the href positional placeholders with their actual value. As
        # such, the order of the URI positional params and the provided
        # function args MUST MATCH.
        for i in range(len(posArgMatches)):
            non_templated_href = non_templated_href.replace("{%s}" % posArgMatches[i], args[i])

        # If we have any URI query params in the href template then...
        if kwArgMatches:
            uriParams = kwArgRegEx.sub('', non_templated_href)
            if '?' in uriParams:
                uriParams = uriParams[uriParams.index('?')+1:]
                uriParams = kwArgRegEx.sub('', uriParams)
                uriParams = uriParams.split('&')

                for param in uriParams:
                    pair = param.split("=")
                    if not pair:
                        continue
                    if pair[0] not in kwargs:
                        kwargs[pair[0]] = pair[1] if len(pair) == 2 else ''

            non_templated_href = kwArgRegEx.sub('', non_templated_href)
            if '?' in non_templated_href:
                non_templated_href = non_templated_href[:non_templated_href.index('?')]
        dict_ = send(method, ctx, non_templated_href, json_data=body, **kwargs)
        inst = ResourceInstance()

        inst._from_response(ctx, dict_)

        return inst
    return fn


class Conn(object):
    def __init__(self, ctx):
        self._ctx = ctx
        self._gateways = {}
        self._affordances = {}
        self.ping() # Calls the Conn to get all possible resources and their affordances.

    def ping(self):
        resp = send('options', self._ctx, '/')
        for key, val in resp.items():
            res = Resource()
            if key in self._gateways:
                res = self._gateways[key]
            for aff in val:
                method = aff.get('method', 'get')
                templated = aff.get('templated', False)
                name = aff.get('name', '')
                href = aff.get('href', '')


                res._add_affordance(name, create_affordance(self._ctx, method, href, templated))
            self._gateways[key] = res

    def __getattr__(self, key):
        return self._gateways[key]
        """
        if key not in self._resources:
            raise KeyError("KeyError: '%s'" % key)
        return self._resources[key]
        """




def main():
    ctx = Context(
        host="http://api.amberengine.dev",
        port="80",
        #public="8abebf3699d76c1707cc192a1627a100888b873e567c85765c0ce52d51129523", # CM ADMIN
        #private="b8c056bc53fa4dcd3665978da53beab6e24a5b64b33f2f625c3c51fb63858130" # CM ADMIN
        public="fa1018e08a53ffcc318b2120d2ffd594eb8e27a9cd53a231160fecedc4adec18",  # Some normal brand
        private="e234a9ed6e43b49715faed62cf51e8d8826b690c3ed84f4fffb4a123798b80e2"  # Some normal brand
    )

    api = Conn(ctx)
    prods = api.products.query(limit=1, owner_type="any")
    p = prods.embedded['products'][0]

    print(p.state["identity"]["name"])
    p.state["identity"]["name"] = "foo"
    import pprint
    import pudb; pu.db
    p = p.update()
    print(p)
    print(p.state["identity"]["name"])


    """lst = api.query("api_keys", limit=5, offset=20)
    keys = lst.embedded['api_keys']
    print("Conn Key IDs: %s" % ", ".join([str(key['id']) for key in keys]))
    key = keys[0]


    key = api.self(key)
    key = api.update(key)

    key = api.update(key)
    product.update()


    api.products['create'](body={})

    api.products.retrieve(412, body={})
    api.products.query(body={'filtering': Predicate()})
    api.products.update("142kjn12jn4k12", body={})
    api.products.patch("412", body={})
    api.products.delete(123, body={})
    api.products.delete(body={"id": [123, 432]})

    prod = api.products.retrieve({}, 412)
    prod = prod.self()
    prod = prod.save()
    prod = prod.delete()


    api.products.save("!23", body={"description": {"keywords": ["my keyword"]}})

    prod._state = {"identity": Object()}
    prod.state
    prod.from_dict()
    prod.from_json()


    prod.identity = {"name": 123, "sku": "54rg34aga"}
    prod.update()
    prod.patch()
    prod.save()



    key = api.update("product", body={"state": "here"})
    api.product.update({}, 1337, owner_type="")
    api.product.id = ""

    api.product.query == Product().query()
    api.product.query == send("product", "GET", dasDasdads)


    key = key.create()
    key = api.api_key.create({"state": "here"})




    key.update()
    key.self()
    lst = api.query("api_keys", limit=5, offset=20)




    key = api.retrieve("api_keys", 1337)
    lst = api.query("products", owner_type="", filtering=None, etc="etc")
    """
    """
    listing = api.products.query(limit=5)
    p = api.products.retrieve(78702)
    print(p)
    #print(p.self()) # return refreshed prod
    """

    """
    print(p['identity']['name'])
    p['identity']['name'] = "foobar"
    print(p['identity']['name'])
    """

    # Still need to support how UPDATES/CREATES work with injecting state into
    # request body.


if __name__ == "__main__":
    main()
