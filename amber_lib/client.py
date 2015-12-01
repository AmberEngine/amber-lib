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
        self.listing = {}
        self.kind = class_.__name__

        json_extract = json.loads(dict_)

        self.hal = json_extract['hal']
        self.total json_extract['total']

        self.count = json_extract.get('count', self.total)
        self.listing = json_extract['_embedded'][self.kind]


    def __len__(self):
        return self.total

    def __getitem__(self, key):
        if isinstance(key, slice):
            start = slice.start
            end = slice.end if slice.end <= self.total else self.total
            step = slice.step if slice.step else 1

            list_ = []
            for index in range(start, end, step):
                list_.append(self.get(index))
            return list_
        else:
            return self.get(key)

    def __iter__(self):
        pass

    def get(self, index):
        if index in self.listing:
            return self.listing[index]
        else:
            raise IndexError()

    def next():
        moar_data = send(GET, self.ctx, self.hal.next.href, None)
        self.list.append(moar_data["_embedded"][self.kind])

    def previous():
        moar_data = send(GET, self.ctx, self.hal.prev.href, None)
        self.list.append(moar_data["_embedded"][self.kind])

    def first():
        moar_data = send(GET, self.ctx, self.hal.first.href, None)
        self.

    def last():
        pass

    def all():
        pass

    def relate():
        pass

    def unrelate():
        pass

    def delete():
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
    url = "%s:%s/%s" % (context.host, context.port, endpoint)

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
