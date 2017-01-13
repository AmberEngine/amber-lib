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
    def __init__(self, ctx):
        super(Resource, self).__init__()

        self.ctx = ctx
        self.affordances = {}
        self.state = {}
        self.embedded = {}
        self.unsaved_state_keys = set()

    def update(self, dict_):
        for k in dict_:
            self.unsaved_state_keys.add(k)

        return super(Resource, self).update(dict_)

    def _add_affordance(self, name, fn):
        self.affordances[name] = fn

    def __getattr__(self, key):
        if key not in self.affordances:
            raise AttributeError("'%s' has no affordance '%s'" % (self.__class__.__name__, key))
        return self.affordances[key]

    def __getitem__(self, key):
        if key == 'embeddded':
            return self.embedded

        if key in self.state:
            return self.state[key]

        raise KeyError("'%s'" % key)

    def __setitem__(self, key, value):
        if key == '_embeded':
            self.embedded = value
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
        return json.dumps(self.state, sort_keys=True, indent=4)


def create_affordance(ctx, method, href, templated):
    posArgRegEx = re.compile('{([a-zA-Z0-9_]+)}')
    kwArgRegEx = re.compile('{\?([a-zA-Z0-9_,]+)}')

    def fn(*args, **kwargs):
        if not templated:
            return send(method, ctx, href)

        args = [str(arg) for arg in args]
        kwargs = {k: str(v) for k, v in kwargs.items()}

        posArgMatches = posArgRegEx.findall(href)
        kwArgMatches = []

        kwMatch = kwArgRegEx.findall(href)
        if len(kwMatch) == 1:
            kwArgMatches = kwMatch[0].split(",")

        if len(args) != len(posArgMatches):
            diff = len(args) - len(posArgMatches)
            if diff > 0:
                raise TypeError("Too many positional arguments included: '%s'" % ", ".join(args[:diff]))
            diff *= -1
            raise TypeError("Missing positional arguments: '%s'" % ", ".join(posArgMatches[:diff]))


        if kwargs:
            for key, val in kwargs.items():
                if key not in kwArgMatches:
                    warnings.warn("function argument '%s' not a valid URI query param" % key, UserWarning)

        non_templated_href = href

        for i in range(len(posArgMatches)):
            non_templated_href = non_templated_href.replace("{%s}" % posArgMatches[i], args[i])

        if kwArgMatches:
            non_templated_href = non_templated_href[:non_templated_href.index('?')-1]

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

    def ping(self):
        resp = send('options', self._ctx, '/')
        for key, val in resp.items():
            res = Resource(self._ctx)
            for aff in val:
                method = aff.get('method', 'get')
                templated = aff.get('templated', False)
                name = aff.get('name', '')
                href = aff.get('href', '')

                res._add_affordance(name, create_affordance(self._ctx, method, href, templated))
            self._resources[key] = res

    def __getattr__(self, key):
        if key not in self._resources:
            raise KeyError("KeyError: '%s'" % key)
        return self._resources[key]



def main():
    ctx = Context(
        host="http://api.amberengine.dev",
        port="80",
        public="fa1018e08a53ffcc318b2120d2ffd594eb8e27a9cd53a231160fecedc4adec18",
        private="e234a9ed6e43b49715faed62cf51e8d8826b690c3ed84f4fffb4a123798b80e2"
    )

    api = API(ctx)
    api.ping()
    #print(json.dumps(api.products.query(limit=1)))
    p = api.products.retrieve(78702)
    print(p.self())



if __name__ == "__main__":
    main()
