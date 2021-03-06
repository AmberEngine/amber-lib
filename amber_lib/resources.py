from datetime import datetime
from urllib.parse import quote, urlparse
import base64
import functools
import hashlib
import json
import re
import warnings

import requests

from amber_lib import errors, query


def _def_wrapper_recursion(val):
    if isinstance(val, DictionaryWrapper):
        return val
    if isinstance(val, dict):
        return DictionaryWrapper(val)
    if isinstance(val, EmbeddedList):
        for index, v in enumerate(val):
            val[index] = _def_wrapper_recursion(v)
        return val
    if isinstance(val, (list, tuple)):
        return [_def_wrapper_recursion(e) for e in val]
    return val

class DictionaryWrapper(dict):
    """A dictionary whose items can be accessed using 'dot notation'.

    DictionaryWrapper is a dictionary with overloaded __getattr__ and __setattr__
    methods, allowing access to stored items using both dictionary-access
    and class-attribute dot-notation.

    For example:

        >>> foo = DictionaryWrapper({"fizz": "buzz"})
        >>> print(foo.fizz)
        buzz
        >>> print(foo["fizz"])
        buzz

    Additionally, whenever an item is set into the dict (including at initialization),
    if the value is a dictionary then it is converted into a DictionaryWrapper.
    """

    def __init__(self, dict_=None, *args, **kwargs):
        if not dict_:
            return

        if not isinstance(dict_, dict):
            raise TypeError('\'dict_\' is not a dict')

        for k, v in dict_.items():
            self[k] = v

        super(DictionaryWrapper, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        try:
            return super(DictionaryWrapper, self).__getitem__(key)
        except KeyError:
            raise AttributeError("'%s' not in %s" % (key, list(self.keys())))

    def __setattr__(self, key, value):
        try:
            return super(DictionaryWrapper, self).__setitem__(
                key,
                _def_wrapper_recursion(value)
            )
        except KeyError:
            raise AttributeError("'%s' not in %s" % (key, list(self.keys())))

    def __setitem__(self, key, value):
        return super(DictionaryWrapper, self).__setitem__(
            key,
            _def_wrapper_recursion(value)
        )

    def update(self, dict_):
        """ Override default `update` method to modify any dictionary values.

        Use DictionaryWrapper.__setitem__ method to update all values in the
        provided dictionary, rather than the mixed-in dict.__setitem__, because
        we need to convert all dictionaries in the provided arugment into
        DictionaryWrapper instances themselves.
        """
        if not isinstance(dict_, dict):
            raise TypeError("'%s' object is not iterable" % dict_.__class__.__name__)
        for key, value in dict_.items():
            self[key] = value

    def values(self):
        return list(super().values())


class BaseResource(object):
    """ Represents generic affordances for a single API resource."""

    def __init__(self):
        super(BaseResource, self).__init__()

        self._affordances = {}

    def _add_affordance(self, name, fn):
        self._affordances[name] = fn

    def __getattr__(self, key):
        if key in self._affordances:
            return self._affordances[key]

        raise AttributeError("'%s' does not exist" % key)


class EmbeddedList(list):
    def __init__(self, type_=None, *args, **kwargs):
        if type_ == "products":
            self._pk_field = "guid"
        else:
            self._pk_field = "id"

        self._id_mapping = {} # contains pk->index pairs
        super().__init__(*args, **kwargs)

    def append(self, value):
        super().append(value)
        if hasattr(value, self._pk_field):
            self._id_mapping[getattr(value, self._pk_field)] = len(self) - 1

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if hasattr(value, self._pk_field):
            self._id_mapping[getattr(value, self._pk_field)] = key

    def __delitem__(self, key):
        v = self[key]
        super().__delitem__(key)
        if hasattr(v, self._pk_field):
            del self._id_mapping[getattr(v, self._pk_field)]

    def pk(self, id_, *args):
        if len(args) > 1:
            raise TypeError("pk expected at most 2 arguments, got %i" % len(args))
        if len(args) == 1:
            try:
                return self[self._id_mapping[id_]]
            except (IndexError, KeyError):
                return args[0]
        else:
            return self[self._id_mapping[id_]]

def create_url(context, endpoint, **uri_args):
    """ Create a full URL using the provided components."""

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


def send(method, cfg, endpoint, json_data=None, **uri_params):
    """Execute an HTTP request constructed from the provided parameters.

    The method must be a valid HTTP method. Body data is sent in JSON format,
    and must be `None` or a dictionary. URI Params are key-value pairs which
    must be string-able.
    """
    method = method.lower()

    if cfg.debug:
        uri = endpoint
        if uri_params:
            uri = uri + "?" + "&".join(['%s=%s' % (k,v) for k,v in uri_params.items()])
        cfg.debug('%s: %s' % (
                'amber_lib.resources.send',
                '%s %s (%s)' % (method, uri, 'has body' if json_data else 'no body')
            )
        )

    if method not in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
        raise AttributeError('Bad HTTP method provided: %s' % method)

    def dump(data):
        return json.dumps(data, sort_keys=True, separators=(',', ':'))

    url = create_url(cfg, endpoint, **uri_params)

    # Convert JSON data to a string. If no JSON data, we send an empty object.
    if json_data:
        for k, v in json_data.items():
            if isinstance(v, query.Predicate):
                v = query.WhereItem(pred=v)
            if isinstance(v, query.WhereItem):
                json_data[k] = v.to_dict()

        payload = dump(json_data)
    else:
        payload = '{}'
    current_timestamp = datetime.isoformat(datetime.utcnow())


    auth_string = ''

    # Standard headers that are present for each HTTP request.
    headers = {
            'Accept': 'application/hal+json',
            'Content-Type': 'application/json',
            'Public-Key': cfg.public if cfg.public else '',
            'Timestamp': current_timestamp,
            'URL': url
            }

    if cfg.token:
        # If a JWT token is available, use in-place of signature.
        auth_string = cfg.token
        if cfg.debug:
            cfg.debug('%s: %s' % (
                    'amber_lib.resources.send',
                    'using json web token instead of Public/Private keys'
                )
            )
    else:
        # Create a signiture using the request's headers and the payload
        # data.
        # Encode/decode is required for the hashing/encrypting functions.
        sig = '%s%s%s' % (dump(headers), payload, cfg.private)
        sig = base64.b64encode(
                hashlib.sha256(sig.encode('utf-8')).hexdigest().encode('utf-8')
                ).decode('ascii')
        auth_string = sig

    headers['Authorization'] = 'Bearer %s' % auth_string
    r = None
    # If request fails and status code is any of the following, attempt a rety.
    retry_on = [408, 419, 500, 502, 504]
    attempts = 0

    while attempts < cfg.request_attempts:
        r = getattr(requests, method)(url, data=payload, headers=headers)
        status = r.status_code
        if status == 200:
            try:
                return r.json()
            except ValueError:
                return {}
        elif status == 440 and cfg.on_token_refresh:
            claims = cfg.token.split('.')[1]
            if 4 - len(claims) % 4 > 0:
                claims += '=' * (4 - len(claims) % 4)

            claims_dict = json.loads(base64.b64decode(claims).decode("utf-8"))
            cfg.token = ''
            cfg.token = send(
                "post",
                cfg,
                "/tokens",
                {"public": claims_dict["sub"]}
            )["key"]
            cfg.on_token_refresh(cfg.token)
            return send(method, cfg, endpoint, json_data, **uri_params)
        elif status in retry_on:
            attempts += 1
        else:
            break # No more attempts. We need to error-out.
    error = {}
    try:
        error = r.json()
    except ValueError:
        pass # response did not include any JSON

    if cfg.debug:
        uri = endpoint
        if uri_params:
            uri = uri + "?" + "&".join(['%s=%s' % (k,v) for k,v in uri_params.items()])
        cfg.debug('%s: %s' % (
                'amber_lib.resources.send',
                '%s ...%s (%s) failed with status: %s' % (
                    method,
                    uri,
                    'has body' if json_data else 'no body',
                    r.status_code
                )
            )
        )

    # Try to raise an amber_lib.Error exception.
    status_code = r.status_code
    if status_code in errors.HTTP_ERRORS:
        raise errors.HTTP_ERRORS[status_code](method, url)
    else:
        raise Exception(method, url)


class LinkContainer(DictionaryWrapper):
    def __getattribute__(self, name):
        if name in ['update', 'values']:
            return self.__getattr__(name)
        return super().__getattribute__(name)


class ResourceInstance(DictionaryWrapper):
    """ Represent the state, affordances, and embedded entities for a Resource.

    State will always be a normal dictionary. Any embedded entities will be
    ResourceInstance instances, with their own state, affordances, etc.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._links= LinkContainer()
        self._embedded = DictionaryWrapper()

    def _from_response(self, cfg, dict_):
        def unserialize_link(link_dict):
            method = link_dict.get("method", "get")
            templated = link_dict.get("templated", False)
            name = link_dict.get("name", "")
            href = link_dict.get("href", "")
            body_params = link_dict.get("body_params", {})

            body = {}
            if body_params:
                body.update(body_params)

            kids = {}
            for kid in link_dict.get("children", []):
                l = unserialize_link(kid)
                kids[kid["name"]] = l
            if kids:
                return LinkContainer(kids) # THIS WONT WORK WITH INJECTION STATE!! TODO TODO TODO
            else:
                new_call = functools.partial(
                    create_affordance(
                        cfg,
                        method,
                        href,
                        templated
                    ),
                    body=body
                )
                link = type('Link', (DictionaryWrapper,), {'__call__': new_call})()
                link['method'] = method
                link['href'] = href
                link['templated'] = templated
                return link

        for key, value in dict_.items():
            if key == '_embedded' and isinstance(value, dict):
                for resName, resListing in value.items():
                    if resName not in self._embedded:
                        self._embedded[resName] = EmbeddedList(resName)
                    for embeddedState in resListing:
                        inst = ResourceInstance()
                        inst._from_response(cfg, embeddedState)
                        self._embedded[resName].append(inst)
            elif key == '_links' and isinstance(value, dict):
                if isinstance(value, dict):
                    value = [val for val in value.values()]
                for aff in value:
                    self._links[aff.get('name')] = unserialize_link(aff)
            else:
                self[key] = value

    def __repr__(self):
        return "<%s '%s' at %s>" % (
            'empty' if not self else 'populated',
            self.__class__.__name__,
            hex(id(self))
        )

    def __str__(self):
        """ Print the state of the current Resource (in JSON).

        Print the current state of the Resource as a JSON string. Note that
        embedded resources and afforances are not included.
        """
        return json.dumps(self, sort_keys=True, indent=4)


def create_affordance(cfg, method, href, templated):
    """Create and return a new affordance function based on provided args.

    Create and return a new affordance function, which will be based off
    the context, method,  href, and templated arguments.

    If the href is templated, it's position arguments become *required*.
    In addition, if kwargs are provided that do not match any of the optional
    URI query param keys an error is outputted. (Note that JSON params still
    need to be supported).
    """
    if cfg.debug:
        cfg.debug('%s: %s' % (
                'amber_lib.resources.create_affordance',
                'creating affordance for: %s %s' % (method, href)
            )
        )
    posArgRegEx = re.compile('{([a-zA-Z0-9_]+)}') # Example match: /component/{comp_name}
    kwArgRegEx = re.compile('{[?&]([a-zA-Z0-9_,]+)}') # Example match: /listing{?limit,offset,sort_by}

    def fn(*args, **kwargs):
        """Dynamically generated function for performing an API request.

        This is a dynamically generated function, which utilizes the
        method type, href url, templated boolean, and Context instance from its
        parent scope.
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
                warnings.warn("function kwarg '%s' not a valid URI query param" % key, UserWarning)
            dict_ = send(method, cfg, href, json_data=body, **kwargs)
            inst = ResourceInstance()
            inst._from_response(cfg, dict_)

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
                if cfg.debug:
                    cfg.debug('%s: %s' % (
                            'amber_lib.resources.create_affordance',
                            'too many positional arguments included'
                        )
                    )
                raise TypeError("Too many positional arguments included: '%s'" % ", ".join(args[:diff]))
            diff *= -1

            if cfg.debug:
                cfg.debug('%s: %s' % (
                        'amber_lib.resources.create_affordance',
                        'missing positional argument(s)'
                    )
                )
            raise TypeError("Missing positional arguments: '%s'" % ", ".join(posArgMatches[:diff]))


        if kwargs:
            for key, val in kwargs.items():
                if key not in kwArgMatches:
                    # Output to StdErr whenever a kwarg does not match any of
                    # the specified URI query param keys.
                    warnings.warn("function argument '%s' not a valid URI query param" % key, UserWarning)
                    if cfg.debug:
                        cfg.debug('%s: %s' % (
                                'amber_lib.resources.create_affordance',
                                'function argument \'%s\' not a valid URI query param' % key
                            )
                        )

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
        dict_ = send(method, cfg, non_templated_href, json_data=body, **kwargs)
        inst = ResourceInstance()

        inst._from_response(cfg, dict_)

        return inst
    return fn
