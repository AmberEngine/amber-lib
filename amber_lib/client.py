#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import base64
import copy
from datetime import datetime
import hashlib
import json

import requests
if sys.version_info >= (3,):
    from urllib.parse import quote, urlparse
else:
    from urllib import quote
    from urlparse import urlparse

import amber_lib.errors as errors

DELETE = 'delete'
GET = 'get'
POST = 'post'
PUT = 'put'


class Container(object):
    """ Container is a lazy-loaded list of API entities. Elements can be
    accessed using either an index subscript or a python slice subscript.
    """

    def __add__(self, other):
        """ Concatenate two container instances together and return a new copy
        containing the data from both. This method will first retrieve all
         available entries, à la proactive-loading.
        """
        if not isinstance(other, Container):
            raise TypeError(
                'A Container may only be added with another Container'
            )

        self.all()
        self_copy = copy.copy(self)
        self_copy.values = copy.copy(self.values)

        for val in other:
            self_copy.__append(val)
        return self_copy

    def __append(self, values):
        """ Append either a list, a Container, or an entity to the
        current container.
        """
        if isinstance(values, list):
            offset = self.offset
            if len(values) <= 0:
                return
            for index, value in enumerate(values):
                self.offset += 1
                if isinstance(value, dict):
                    instance = self.class_(self.ctx)
                    obj = instance.from_dict(value)
                else:
                    self.all()
                    obj = value

                self.values[index + offset] = obj
        elif isinstance(values, Container):
            self.all()
            for val in values:
                self.__append(val)
        else:
            values._ctx = self.ctx
            self.all()
            self.values[len(self.values)] = values

    def __contains__(self, item):
        """ Magic method which will return a boolean result indicating True
        if the specified item exists within the Container; false, otherwise.
        This method will first retrieve all available entries, à la
        proactive-loading.
        """
        self.all()
        return item in self.values.values()

    def __delitem__(self, key):
        """ Remove the specified index from the Container. This method will
        first retrieve all available entries, à la proactive-loading.
        """
        self.all()

        if key not in self.values:
            raise IndexError

        for index, value in enumerate(self[key + 1:len(self)]):
            self[key + index] = self[key + index + 1]
        del self.values[len(self) - 1]

    def __getitem__(self, key):
        """ Elements can be retrieved from the Container by specifying either
        an integer index or a slice instance.

        For example, using an integer index:

            first = container[0]
            last = container[-1]
            print(container[5]])

        A Container's elements can also be accessed using slice objects:

            container[1:7]
            container[:]
            container[-5:]
            container[1:100:5]
        """
        if isinstance(key, slice):
            start = key.start if key.start else 0
            end = len(self)
            if key.stop and key.stop <= len(self):
                end = key.stop
            step = key.step if key.step else 1

            container = Container({}, self.class_, self.ctx)
            count = 0
            for index in range(start, end, step):
                # Get next batch of entries.
                container.values[count] = self.__get(index)
                count += 1
            return container
        elif isinstance(key, int):
            return self.__get(key)
        else:
            raise TypeError

    def __init__(self, dict_, class_, ctx, offset=0):
        """ Initialize a new instance of Container, specifying a JSON-HAL
        dictionary, the class the data represents, and a context.
        """
        self.class_ = class_
        self.ctx = ctx
        self.kind = class_._resource
        self.offset = offset
        self.values = {}

        self.hal = dict_.get('_links', {})
        self.total = dict_.get('total', 0)

        self.batch_size = dict_.get('count', self.total)

        embedded = dict_.get('_embedded', {}).get(self.kind, [])
        self.__append(embedded)

    def __iter__(self):
        """ Yield sequential values from the total entries available.
        """
        for val in range(len(self)):
            yield self[val]

    def __len__(self):
        """ Return the total number of readable  database entries.
        """
        if self.total:
            return self.total
        return len(self.values)

    def __reversed__(self):
        """ Return a copy of the current Container with the order of the
        values it contains sorted in reverse order. This method will first
        retrieve all entries, à la proactive-loading.
        """
        self.all()

        self_copy = copy.copy(self)
        self_copy.values = copy.copy(self.values)

        for key in self.values:
            self_copy[key] = self.values[len(self.values) - key - 1]

        return self_copy

    def __setitem__(self, key, value):
        """ Assign a value to an indexable location within the current
        Container. This method will first retrieve all available entries,
        à la proactive-loading.
        """
        self.all()
        if key not in self.values:
            raise IndexError
        self.values[key] = value

    def __get(self, index):
        """ Retrieve a value at the provided index from the Container. Negative
        indices will operate relatively to the end of the Container.
        """
        if index < 0:
            if abs(index) >= len(self):
                raise IndexError()
            index += len(self)

        if index >= len(self):
            raise IndexError()

        if index in self.values:
            return self.values[index]
        else:
            can_continue = True
            if index > (self.offset - 1):
                while index > (self.offset - 1) and can_continue:
                    can_continue = self.__next()
            elif index < self.offset:
                while index < self.offset and can_continue:
                    can_continue = self.__previous()

            return self.values[index]

    def __next(self):
        """ Retrieve the next batch of entries from the API using the HAL
        next-href link endpoint.
        """
        if self.hal is None or 'next' not in self.hal:
            return False

        more_data = send(GET, self.ctx, self.hal['next']['href'], self.hal['next']['params'])
        self.hal = more_data.get('_links', {})
        embedded = more_data.get('_embedded', {}).get(self.kind, [])

        self.__append(embedded)

    def __prepend(self, values):
        """ Prepend a list, Container or an entry to the current Container's
        values.
        """
        if isinstance(values, list):
            for index, value in enumerate(values):
                self.all()
                obj = value

                self.values[index + self.offset] = obj
        elif isinstance(values, Container):
            self.all()
            self.values = (values + self).values
        else:
            values._ctx = self.ctx
            self.all()

            for index, val in enumerate(reversed(self)):
                self.values[index + 1] = val

            self[0] = values

    def __previous(self):
        """ Retrieve the previous batch of entries from the API using the HAL
        previous-href link endpoint.
        """
        if self.hal is None or 'previous' not in self.hal:
            return False

        moar_data = send(GET, self.ctx, self.hal['previous']['href'], self.hal['previous']['params'])
        self.hal = moar_data.get('_links', {})
        embedded = moar_data.get('_embedded', {}).get(self.kind, [])

        self.offset -= self.batch_size
        if self.offset < 0:
            self.offset = 0

        self.__prepend(embedded)

    def all(self):
        """ Retrieve all possible entries from the current Container.
        """
        ret = self[:]

        self.hal = {}
        self.batch_size = 0
        self.total = None

        return ret

    def append(self, value):
        """ Append a value to the end of the current Container. This method
        will retrieve all available entries, à la proactive-loading.
        """
        self.all()
        self.values[len(self.values)] = value

    def count(self):
        """ Return the current length of the Container.
        """
        return len(self)

    def delete(self):
        self.all()
        for entity in self:
            entity.delete()

    def extend(self, list_):
        """ Append an existing list or container to the current Container
        instance.
        """
        self.__append(list_)

    def index(self, item):
        """ Retrieve the integer index number where the first instance of the
        provided item can be found.
        """
        for key, val in enumerate(self):
            if val == item:
                return key
        raise ValueError

    def insert(self, insert_index, item):
        """ Insert the provided item at the specified index. This method will
        retrieve all available entries, à la proactive-loading.
        """
        self.all()
        for index, val in enumerate(reversed(self)):
            if index >= insert_index:
                break
            self.values[index + insert_index + 1] = val

        self.values[insert_index] = item

    def to_json(self):
        """ Retrieve a JSON string of all currently loaded model's dictionary
        representations.
        """
        return json.dumps(self.to_list())

    def to_list(self):
        """ Retrieve a list of all currently loaded models as dictionary
        objects.
        """
        list_ = []
        for index in sorted(self.values.keys()):
            list_.append(self[index].to_dict())

        return list_

    def pop(self, index=None):
        """ Retrieve and remove the last index from the Collection.
        """
        if index is None:
            index = len(self) - 1

        val = self[index]
        del self[index]

        return val

    def set_relation(self, type_, thing):
        """ Set or unset a relation between all the elements contained within
        the Container and the thing being related to.
        """
        first = [str(entry.id) for entry in self]
        if isinstance(thing, Container):
            second = [str(entry.id) for entry in thing]
        else:
            second = [str(thing.id)]

        res1 = self[0]._resource
        if isinstance(thing, Container):
            res2 = thing[0]._resource
        else:
            res2 = thing._resource

        payload = send(
            type_,
            self.ctx,
            '/relations',
            None,
            **{
                res1: ','.join(first),
                res2: ','.join(second)
            }
        )

    def relate(self, thing):
        """ Create a relation between the Container's contained elements and
        the thing.
        """
        self.set_relation(POST, thing)

    def unrelate(self, thing):
        """ Uncreate a relation between the current Container's contained
        collection of elements.
        """
        self.set_relation(DELETE, thing)

    def remove(self, item):
        """ Remove the first instance of the item specified.
        """
        del self[self.index(item)]

    def reverse(self):
        """ Perform an in-place reversal of the ordering of the values in the
        Container.
        """
        for key, val in enumerate(reversed(self)):
            self.values[key] = val


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
    """ Send a data request to a resource on API, based on the context,
    endpoint, JSON data and optional URI parameter values. This method will
    attempt to retry on certain server errors. A JSON dictionary of the
    response will be returned.
    """
    method = method.lower()
    if method not in ['get', 'post', 'put', 'delete']:
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
        print(payload)
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
            sub = json.loads(base64.b64decode(claims).decode('utf-8'))['sub']
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
        if status_code in errors.HTTP_ERRORS:
            raise errors.HTTP_ERRORS[status_code](
                error['code'],
                error['title'],
                error['message']
            )
        else:
            raise Exception(error['code'], error['title'], error['message'])
    except ValueError:
        raise Exception(r.status_code, url)
