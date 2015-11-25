# imports

def create_payload(context, url, data):
    payload = {
        "public_key": context.public,
        "url": url,
        "timestamp": datetime.isoformat(datetime.utcnow()),
        "headers": {'Content-Type': 'application/json'},
        "data": data
    }


    jdump = json.dumps(payload, sort_keys=True, seperators=(',', ':'))

    sig = base64.b64encode(
        hashlib.sha256(jdump + context.private).hexdigest()
    )

    payload["signature"] = sig

    return json.dumps(payload)


def create_url(context, endpoint, **uri_args):
    """ Create a full URL using the context settings, the desired endpoint,
    and any option URI (keyword) arguments.
    """
    url = "%s:%s%s" % (context.host, context.port, endpoint)

    if len(uri_args) > 0:
        url += "?"
        query_params = []
        for key, val in uri_args.iteritems():
            query_params.append("%s=%s" % (key, val))

        url += "&".join(query_params)

    return url



def get(context, endpoint, json_data, **uri_args):
    url = create_url(context, endpoint, uri_params)
    payload = create_payload(context, url, json_data)

    r = requests.get(url, data=payload)
    if r.status_code != 200:
        error = json.loads(r.text)
        raise Exception(error["code"], error["title"], error["message"])

    return json.loads(r.text)

def post(context, endpoint, json_data, **uri_args):
    url = create_url(context, endpoint, uri_params)
    payload = create_payload(context, url, json_data)

    r = requests.post(url, data=payload)
    if r.status_code != 200:
        error = json.loads(r.text)
        raise Exception(error["code"], error["title"], error["message"])

    return json.loads(r.text)

def put(context, endpoint, json_data, **uri_args):
    url = create_url(context, endpoint, uri_params)
    payload = create_payload(context, url, json_data)

    r = requests.put(url, data=payload)
    if r.status_code != 200:
        error = json.loads(r.text)
        raise Exception(error["code"], error["title"], error["message"])

    return json.loads(r.text)


def delete(context, endpoint, json_data, **uri_args):
    url = create_url(context, endpoint, uri_params)
    payload = create_payload(context, url, json_data)

    r = requests.delete(url, data=payload)
    if r.status_code != 200:
        error = json.loads(r.text)
        raise Exception(error["code"], error["title"], error["message"])

    return json.loads(r.text)


