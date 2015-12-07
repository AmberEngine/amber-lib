import base64
import json
import hashlib
from datetime import datetime
import copy

import requests


GET = 'get'
POST = 'post'
PUT = 'put'
DELETE = 'delete'


class Container(object):
    """ Container is a lazy-loaded list of API resources. Elements can be accessed
    using either an index subscript or a python slice subscript.
    """

    def __init__(self, dict_, class_, ctx, offset=0):
        """ Initialize a new instance of Container, specifying a JSON-HAL
        dictionary, the class the data represents, and a context.
        """
        self.ctx = ctx
        self.values = {}
        self.class_ = class_
        self.kind = class_.__name__.lower()

        self.offset = offset

        self.hal = dict_.get('_links', {})
        self.total = dict_.get('total')

        self.batch_size = dict_.get('count', self.total)

        embedded = dict_.get('_embedded', {}).get(self.kind + 's', [])
        self.__append(embedded)

    def __add__(self, other):
        if not isinstance(other, Container):
            raise TypeError('"NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO!" -D.V.')

        self.__finish_it()
        self_copy = copy.copy(self)
        self_copy.values = copy.copy(self.values)
        for val in other:
            self_copy.__append(val)
        return self_copy

    def __contains__(self, item):
        return item in self.values.values()

    def __delitem__(self, key):
        self.__finish_it()
        del self.values[key]
        for i in range(len(self) - key - 1):
            self.values[key + i] = self.values[key + i + 1]

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
        else:
            return self.__get(key)

    def __iter__(self):
        """ Yeild sequential values from the total entries available.
        """
        for val in range(len(self)):
            yield self[val]

    def __le__(self, other):
        return "le API > %s" % (other,)

    def __len__(self):
        """ Return the total number of accessible database entries.
        """
        if self.total:
            return self.total
        return len(self.values)

    def __pow__(self, other):
        return "It's a me! Mario!" * other

    def __reversed__(self):
        self.__finish_it()
        dict_ = []

        for key in self.values:
            dict_[key] = self.values[len(self.values) - key - 1]

        return dict_

    def __setitem__(self, key, value):
        self.__finish_it()
        self.values[key] = value

    def __all(self):
        return self[:]

    def __append(self, values):
        if isinstance(values, list):
            offset = self.offset
            for index, value in enumerate(values):
                self.offset += 1
                obj = self.class_(self.ctx).from_dict(value)
                self.values[index + offset] = obj
        elif isinstance(values, Container):
            self.__finish_it()
            for val in values:
                self.__append(val)
        else:
            values._ctx = self.ctx
            self.values[len(self.values)] = values

    def __finish_it(self):
        if self.total is not None:
            self.__all()
        self.hal = {}
        self.batch_size = 0
        self.total = None

    def __get(self, index):
        # Deal with negative indexes: if |index| < total, adjust index to
        # become positive, and retrieve. Otherwise, raise error.
        if index < 0:
            if abs(index) > len(self):
                raise IndexError()
            index += len(self)

        if index > len(self):
            raise IndexError()

        if index in self.values:
            return self.values[index]
        else:
            if index > (self.offset - 1):
                while index > (self.offset - 1):
                    self.__next()
            elif index < self.offset:
                while index < self.offset:
                    self.__previous()
            return self.values[index]

    def __next(self):
        if 'next' not in self.hal:
            return False

        moar_data = send(GET, self.ctx, self.hal['next']['href'], None)
        self.hal = moar_data.get('_links', {})
        embedded = moar_data.get('_embedded', {}).get(self.kind + 's', [])

        self.__append(embedded)

    def __prepend(self, values):
        if isinstance(values, list):
            for index, value in enumerate(values):
                obj = self.class_(self.ctx).from_dict(value)
                self.values[self.offset + index] = obj
        elif isinstance(values, dict):
            pass

    def __previous(self):
        if 'prev' not in self.hal:
            return False

        moar_data = send(GET, self.ctx, self.hal['prev']['href'], None)
        self.hal = moar_data.get('_links', {})
        embedded = moar_data.get('_embedded', {}).get(self.kind + 's', [])

        self.offset -= self.batch_size
        if self.offset < 0:
            self.offset = 0

        self.__prepend(embedded)

    def append(self, value):
        self.__finish_it()
        self.values[len(self.values)] = value

    def count(self):
        return len(self)

    def extend(self, list_):
        self.__append(list_)

    def index(self, item):
        for key, val in enumerate(self):
            if val == item:
                return key
        raise Exception("nope")

    def insert(self, index, item):
        self[index] = item

    def pop(self, index=None):
        if index is None:
            index = len(self) - 1

        val = self[index]
        del self[index]

        return val

    def remove(self, item):
        del self[item]

    def reverse(self):
        for key, val in enumerate(reversed(self)):
            self.values[key] = val


def create_payload(context, url, data):
    payload = {
        'public_key': context.public,
        'url': url,
        'timestamp': datetime.isoformat(datetime.utcnow()),
        'headers': {'Content-Type': 'application/json'},
        'data': data
    }

    jdump = json.dumps(payload, sort_keys=True, separators=(',', ':'))

    sig = base64.b64encode(
        hashlib.sha256(jdump + context.private).hexdigest()
    )

    payload['signature'] = sig

    return json.dumps(payload)


def create_url(context, endpoint, **uri_args):
    """ Create a full URL using the context settings, the desired endpoint,
    and any option URI (keyword) arguments.
    """
    if not endpoint:
        endpoint = ''
    url = '%s:%s%s' % (context.host, context.port, endpoint)

    if len(uri_args) > 0:
        url += '?'
        query_params = []
        for key, val in uri_args.iteritems():
            query_params.append('%s=%s' % (key, val))

        url += '&'.join(query_params)
    return url


def send(method, ctx, endpoint, json_data, **uri_params):
    method = method.lower()
    if method not in ['get', 'post', 'put', 'delete']:
        raise AttributeError('Bad method')

    url = create_url(ctx, endpoint, **uri_params)
    payload = create_payload(ctx, url, json_data)

    r = getattr(requests, method)(url, data=payload)
    if r.status_code != 200:
        error = r.json()
        raise Exception(error['code'], error['title'], error['message'])
    return r.json()
