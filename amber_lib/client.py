import base64
import json
import hashlib
from datetime import datetime

import requests

GET = "get"
POST = "post"
PUT = "put"
DELETE = "delete"


class Collection(object):
    def __init__(self, dict_, class_, ctx):
        self.ctx = ctx
        self.values = {}
        self.class_ = class_
        self.kind = class_.__name__.lower()

        #json_extract = json.loads(dict_)

        self.hal = dict_.get('_links', {})
        self.total = dict_.get('total')

        self.count = dict_.get('count', self.total)
        for index, value in enumerate(dict_.get('_embedded', {}).get(self.kind + 's', [])):
            self.values[index] = class_(ctx).from_dict(value)

    def __len__(self):
        return self.total

    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start if key.start else 0
            end = self.total
            if key.stop and key.stop <= self.total:
                end = key.stop
            step = key.step if key.step else 1

            list_ = []
            for index in range(start, end, step):
                list_.append(self.get(index))
            return list_
        else:
            return self.get(key)

    def __iter__(self):
        pass

    def get(self, index):
        if index in self.values:
            return self.values[index]
        else:
            if index < self.total:
                self.next()
                return self.values[index]
            else:
                raise IndexError()

    def append(self, values):
        if isinstance(values, list):
            size = len(self.values)
            for index, value in enumerate(values):
                self.values[size + index] =\
                    self.class_(self.ctx).from_dict(value)
        elif isinstance(values, dict):
            pass

    def prepend(self, values):
        if isinstance(values, list):
            pass
        elif isinstance(values, dict):
            pass

    def next(self):
        moar_data = send(GET, self.ctx, self.hal['next']['href'], None)
        self.hal = moar_data.get('_links', {})
        self.append(moar_data.get("_embedded", {}).get(self.kind + 's', []))

    def previous(self):
        moar_data = send(GET, self.ctx, self.hal['prev']['href'], None)
        self.prepend(moar_data.get("_embedded", {}).get(self.kind + 's', []))

    def first(self):
        moar_data = send(GET, self.ctx, self.hal['first']['href'], None)

    def last(self):
        pass

    def all(self):
        pass

    def relate(self):
        pass

    def unrelate(self):
        pass

    def delete(self):
        pass


def create_payload(context, url, data):
    payload = {
        "public_key": context.public,
        "url": url,
        "timestamp": datetime.isoformat(datetime.utcnow()),
        "headers": {'Content-Type': 'application/json'},
        "data": data
    }

    jdump = json.dumps(payload, sort_keys=True, separators=(',', ':'))

    sig = base64.b64encode(
        hashlib.sha256(jdump + context.private).hexdigest()
    )

    payload["signature"] = sig

    return json.dumps(payload)


def create_url(context, endpoint, **uri_args):
    """ Create a full URL using the context settings, the desired endpoint,
    and any option URI (keyword) arguments.
    """
    if not endpoint:
        endpoint = ''
    url = "%s:%s%s" % (context.host, context.port, endpoint)

    if len(uri_args) > 0:
        url += "?"
        query_params = []
        for key, val in uri_args.iteritems():
            query_params.append("%s=%s" % (key, val))

        url += "&".join(query_params)
    return url


def send(method, ctx, endpoint, json_data, **uri_params):
    method = method.lower()
    if method not in ["get", "post", "put", "delete"]:
        raise AttributeError("Bad method")

    url = create_url(ctx, endpoint, **uri_params)
    payload = create_payload(ctx, url, json_data)

    r = getattr(requests, method)(url, data=payload)
    if r.status_code != 200:
        error = json.loads(r.text)
        raise Exception(error["code"], error["title"], error["message"])

    return json.loads(r.text)
