import base64
import json
import hashlib
from datetime import datetime

import requests


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
