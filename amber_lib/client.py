#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import copy
from datetime import datetime
import hashlib
import json

import requests

DELETE = 'delete'
GET = 'get'
POST = 'post'
PUT = 'put'


class Container(object):
    """ Container is a lazy-loaded list of API entities. Elements can be
    accessed using either an index subscript or a python slice subscript.
    """

    def __init__(self, dict_, class_, ctx, offset=0):
        """ Initialize a new instance of Container, specifying a JSON-HAL
        dictionary, the class the data represents, and a context.
        """
        self.class_ = class_
        self.ctx = ctx
        self.kind = class_.__name__.lower()
        self.offset = offset
        self.values = {}

        self.hal = dict_.get('_links', {})
        self.total = dict_.get('total')

        self.batch_size = dict_.get('count', self.total)

        embedded = dict_.get('_embedded', {}).get(self.kind + 's', [])
        self.__append(embedded)

    def __add__(self, other):
        """ Magic method __add__ will concatenate two container instances
        together and return a new copy contain the data from both. This method
        will first retrieve all available entries, à la proactive-loading.
        """
        if not isinstance(other, Container):
            raise TypeError('"NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO!" -D.V.')

        self.__finish_it()
        self_copy = copy.copy(self)
        self_copy.values = copy.copy(self.values)

        for val in other:
            self_copy.__append(val)
        return self_copy

    def __contains__(self, item):
        """ Magic method which will return a boolean result indicating True
        if the specified item exists within the Container; false, otherwise.
        This method will first retrieve all available entries, à la
        proactive-loading.
        """
        self.__finish_it()
        return item in self.values.values()

    def __delitem__(self, key):
        """ Magic method which will attempt to remove the specifid index
        from the Container. This method will first retrieve all available
        entries, à la proactive-loading.
        """
        self.__finish_it()

        if key not in self.values:
            raise IndexError

        for index, value in enumerate(self[key + 1:len(self)]):
            self[key + index] = self[key + index + 1]
        del self.values[len(self) - 1]

    def __getitem__(self, key):
        """ Elements can be retrieved from the Container by specifying either
        an integer index or a slice instance.

        For example, using an integer index:

            collection = magically_get_a_collection(...)

            first = collection[0]
            last = collection[-1]
            print(collection[5]])

        A Container's elements can also be accessed using slice objects:

            collection = magically_get_a_collection(...)
            collection[1:7]
            collection[:]
            collection[-5:]
            collection[1:100:5]

        """
        if isinstance(key, slice):
            start = key.start if key.start else 0
            end = len(self)
            if key.stop and key.stop <= len(self):
                end = key.stop
            step = key.step if key.step else 1

            list_ = Container({}, self.class_, self.ctx)
            for index in range(start, end, step):
                # Get next batch of entries.
                list_.append(self.__get(index))
            return list_
        elif isinstance(key, int):
            return self.__get(key)
        else:
            raise TypeError

    def __iter__(self):
        """ Magic method for yeilding sequential values from the total
        entries available.
        """
        for val in range(len(self)):
            yield self[val]

    def __le__(self, other):
        """ Magic method for humour & reddit.
        """
        return "le API > %s" % (other,)

    def __len__(self):
        """ Magic method for returning the total number of accessible
        database entries.
        """
        if self.total:
            return self.total
        return len(self.values)

    def __pow__(self, other):
        """ Magic method for N64 nostalgia.
        """
        return "It's a me! Mario!" * other

    def __reversed__(self):
        """ Magic method for returning a copy of the current Container, with
        the order of the values it contains sorted in reverse order. This
        method will first retrieve all entries, à la proactive-loading.
        """
        self.__finish_it()

        self_copy = copy.copy(self)
        self_copy.values = copy.copy(self.values)

        for key in self.values:
            self_copy[key] = self.values[len(self.values) - key - 1]

        return self_copy

    def __setitem__(self, key, value):
        """ Magic method for assigning a particular value to an available
        indexable location within the current Container. This method will
        first retrieve all available entries, à la proactive-loading.
        """
        self.__finish_it()
        if key not in self.values:
            raise IndexError
        self.values[key] = value

    def __all(self):
        """ Retrieve all possible entries from the current Container.
        """
        return self[:]

    def __append(self, values):
        """ Append either a list, a Container, or an entity to the
        current container.
        """
        if isinstance(values, list):
            offset = self.offset
            for index, value in enumerate(values):
                self.offset += 1
                if isinstance(value, dict):
                    instance = self.class_(self.ctx)
                    obj = instance.from_dict(value)
                else:
                    self.__finish_it()
                    obj = value

                self.values[index + offset] = obj
        elif isinstance(values, Container):
            self.__finish_it()
            for val in values:
                self.__append(val)
        else:
            values._ctx = self.ctx
            self.__finish_it()
            self.values[len(self.values)] = values

    def __finish_it(self):
        """ It's dangerous to go alone! Take all these entries! Retrieve all
        the things!
        """
        if self.total is not None and self.total > len(self.values):
            self.__all()
        self.hal = {}
        self.batch_size = 0
        self.total = None

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

        more_data = send(GET, self.ctx, self.hal['next']['href'], None)
        self.hal = more_data.get('_links', {})
        embedded = more_data.get('_embedded', {}).get(self.kind + 's', [])

        self.__append(embedded)

    def __prepend(self, values):
        """ Prepend a list, Container or an entry to the current Container's
        values.
        """
        if isinstance(values, list):
            for index, value in enumerate(values):
                self.__finish_it()
                obj = value

                self.values[index + self.offset] = obj
        elif isinstance(values, Container):
            self.__finish_it()
            self.values = (values + self).values
        else:
            values._ctx = self.ctx
            self.__finish_it()

            for index, val in enumerate(reversed(self)):
                self.values[index + 1] = val

            self[0] = values

    def __previous(self):
        """ Retrieve the previous batch of entries from the API using the HAL
        previous-href link endpoint.
        """
        if self.hal is None or 'previous' not in self.hal:
            return False

        moar_data = send(GET, self.ctx, self.hal['previous']['href'], None)
        self.hal = moar_data.get('_links', {})
        embedded = moar_data.get('_embedded', {}).get(self.kind + 's', [])

        self.offset -= self.batch_size
        if self.offset < 0:
            self.offset = 0

        self.__prepend(embedded)

    def append(self, value):
        """ Append a value to the end of the current Container. This method
        will retrieve all available entries, à la proactive-loading.
        """
        self.__finish_it()
        self.values[len(self.values)] = value

    def count(self):
        """ Return the current length of the Container.
        """
        return len(self)

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
        self.__finish_it()
        for index, val in enumerate(reversed(self)):
            if index >= insert_index:
                break
            self.values[index + insert_index + 1] = val

        self.values[insert_index] = item

    def pop(self, index=None):
        """ Retrieve and remove the last index from the Collection.
        """
        if index is None:
            index = len(self) - 1

        val = self[index]
        del self[index]

        return val

    def set_relation(self, type_, thing):
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
            "/relations",
            None,
            **{
                res1: ",".join(first),
                res2: ",".join(second)
            }
        )

    def relate(self, thing):
        self.set_relate(POST, thing)

    def unrelate(self, thing):
        self.set_relate(DELETE, thing)

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
    host = ""
    port = ""
    private = ""
    public = ""
    request_attempts = 3

    def __init__(self, **kwargs):
        """ Create a new instance of Context, using keyword arguments to
        override class defaults.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


def create_payload(context, url, data):
    """ Generate a new dictionary payload based on a context, url and data
    dictionary.
    """
    payload = {
        'data': data,
        'headers': {'Content-Type': 'application/json'},
        'public_key': context.public,
        'timestamp': datetime.isoformat(datetime.utcnow()),
        'url': url
    }

    jdump = json.dumps(
        payload,
        sort_keys=True,
        separators=(',', ':')
    ).encode('utf-8')

    hash_ = hashlib.sha256(jdump)
    hash_.update(context.private.encode('utf-8'))
    digest = hash_.hexdigest().encode('ascii')

    sig = base64.b64encode(
        digest
    )

    payload['signature'] = sig.decode('ascii')

    return json.dumps(payload, sort_keys=True, separators=(',', ':'))


def create_url(context, endpoint, **uri_args):
    """ Create a full URL using the context settings, the desired endpoint,
    and any option URI (keyword) arguments.
    """
    url = '%s:%s%s' % (context.host, context.port, endpoint)

    if len(uri_args) > 0:
        url += '?'
        query_params = []
        for key in sorted(uri_args.keys()):
            query_params.append('%s=%s' % (key, uri_args[key]))

        url += '&'.join(query_params)
    return url


def send(method, ctx, endpoint, json_data, **uri_params):
    """ Send a data request to a resource on API, based on the context,
    endpoint, JSON data and optional URI parameter values. This method will
    attempt to retry on certain server errors. A JSON dictionary of the
    response will be returned.
    """
    method = method.lower()
    if method not in ['get', 'post', 'put', 'delete']:
        raise AttributeError('Bad method')

    url = create_url(ctx, endpoint, **uri_params)
    payload = create_payload(ctx, url, json_data)

    retry_on = [408, 419, 500, 502, 504]
    attempts = 0
    r = None
    while attempts < ctx.request_attempts:
        r = getattr(requests, method)(url, data=payload)
        status = r.status_code
        if status == 200:
            try:
                return r.json()
            except ValueError:
                return {}
        elif status in retry_on:
            attempts += 1
        else:
            break

    try:
        error = r.json()
        raise Exception(error['code'], error['title'], error['message'])
    except ValueError:
        Exception(r.status_code, url)
