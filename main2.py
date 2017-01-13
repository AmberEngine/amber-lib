from datetime import datetime
import base64
import copy
import hashlib
import json
import re
import warnings

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
    def __init__(self, code, title, description):
        self.code = code
        self.title = title
        self.description = description

        Exception.__init__(self, self.description)


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

    try:
        error = r.json()
        status_code = r.status_code
        if status_code in HTTP_ERRORS:
            raise HTTP_ERRORS[status_code](
                    error['code'],
                    error['title'],
                    error['message']
                    )
        else:
            raise Exception(error['code'], error['title'], error['message'])
    except ValueError:
        raise Exception(r.status_code, url)


class Context(object):
    """ Context contains contextual data for generating data requests to the
    API. Used for determining which API is being hit, contains authentication
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


class Resource(dict):
    """ A Resource instance is made up by an internal state, any embedded
    external resources, and any affordances for the current resource.
    The state can be accessed via dictionary-notation (eg: res['id']), while
    the affordance functions can be accessed like normal methods.

    Note that `unsaved_state_keys` is not operational.
    Note that there may be method naming collisions (like 'update').
    Note that inserting the current state of the resource into outbound
    affordance requests has not been implemented yet (so no "update" or "create"
    functionallity).
    """
    def __init__(self, ctx):
        super(Resource, self).__init__()

        self.ctx = ctx
        self.affordances = {}
        self.state = {}
        self.embedded = {}
        self.unsaved_state_keys = set() # not really used for anything yet

    def update(self, dict_):
        # Probobly a naming conflict with "update" affordances.
        for k in dict_:
            self.unsaved_state_keys.add(k)

        return super(Resource, self).update(dict_)

    def _add_affordance(self, name, fn):
        self.affordances[name] = fn

    def __getattr__(self, key):
        """ The only attributes accessible from a resource should be inheritted
        dictionary methods, and affordances.
        """
        if key not in self.affordances:
            raise AttributeError("'%s' has no affordance '%s'" % (self.__class__.__name__, key))
        # Can inheritted dictionary methods be used? Or does this prevent them?
        return self.affordances[key]

    def __getitem__(self, key):
        if key == 'embedded':
            return self.embedded

        if key in self.state:
            return self.state[key]

        raise KeyError("'%s'" % key)

    def __setitem__(self, key, value):
        if key == '_embedded':
            for resName, list_ in value.items():
                for dict_ in list_:
                    inst = Resource(self.ctx)
                    for k, v in dict_.items():
                        inst[k] = v
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
                self._add_affordance(name, create_affordance(self.ctx, method, href, templated))
        else:
            self.unsaved_state_keys.add(key)
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
        """ Printing a Resource instance will result in printing *just* the current
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
        This function will result in a HTTP call to the API.
        Postional args replace tempalted positional URI args, while kwargs
        replace option URI query parameters (and eventually JSON body params).
        """

        if not templated:
            # href is not tempalted, so we can just do the HTTP call.
            return send(method, ctx, href)

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
        dict_ = send(method, ctx, non_templated_href, **kwargs)
        inst = Resource(ctx)

        for key, val in dict_.items():
            inst[key] = val
        inst.unsaved_state_keys = set() # reset unsaved state keys, since we just updated all of them

        return inst
    return fn


class API(object):
    def __init__(self, ctx):
        self._ctx = ctx
        self._resources = {}
        self._affordances = {}
        self.ping() # Calls the API to get all possible resources and their affordances.

    def _create_affordance_wrapper(self, aff_name):
        def fn(thing, *args, **kwargs):
            res = thing
            if isinstance(thing, str):
                if thing not in self._affordances[aff_name]:
                    raise KeyError("'%s' does not have affordance '%s'" % (thing, aff_name))
                res = self._resources[thing]
            elif not isinstance(thing, Resource):
                raise TypeError("'%s' must be a string or a Resource object" % thing.__class__.__name__)
            return res.__getattr__(aff_name)(*args, **kwargs)
        return fn

    def ping(self):
        resp = send('options', self._ctx, '/')
        for key, val in resp.items():
            res = Resource(self._ctx)
            for aff in val:
                method = aff.get('method', 'get')
                templated = aff.get('templated', False)
                name = aff.get('name', '')
                href = aff.get('href', '')

                if name not in self._affordances:
                    self._affordances[name] = set()
                self._affordances[name].add(key)

                res._add_affordance(name, create_affordance(self._ctx, method, href, templated))
            self._resources[key] = res

    def __getattr__(self, key):
        if key not in self._affordances:
            raise KeyError("KeyError: '%s'" % key)
        return self._create_affordance_wrapper(key)
        """
        if key not in self._resources:
            raise KeyError("KeyError: '%s'" % key)
        return self._resources[key]
        """




def main():
    ctx = Context(
        host="http://api.amberengine.dev",
        port="80",
        public="8abebf3699d76c1707cc192a1627a100888b873e567c85765c0ce52d51129523", # CM ADMIN
        private="b8c056bc53fa4dcd3665978da53beab6e24a5b64b33f2f625c3c51fb63858130" # CM ADMIN
        #public="fa1018e08a53ffcc318b2120d2ffd594eb8e27a9cd53a231160fecedc4adec18",  # Some normal brand
        #private="e234a9ed6e43b49715faed62cf51e8d8826b690c3ed84f4fffb4a123798b80e2"  # Some normal brand
    )

    api = API(ctx)
    # api.query("products", limit=5)
    # p = api.retrieve("products", 78702)

    # p2 = api.update(p)

    # Retrieve some API Keys and refresh one of them...
    lst = api.query("api_keys", limit=5, offset=20)
    keys = lst.embedded['api_keys']
    print("API Key IDs: %s" % ", ".join([str(key['id']) for key in keys]))
    key = keys[0]
    key.self()

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
