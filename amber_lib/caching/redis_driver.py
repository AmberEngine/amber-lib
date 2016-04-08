#Embedded file name: /Users/curtislagraff/.virtualenvs/amber-lib/amber-lib/amber_lib/caching/redis_driver.py
import json
import redis
AGE_KEY = '__cache_max_age'

def cache_resource(opts, uri, resource, max_age):
    if 'host' not in opts:
        raise Exception('Missing "host" in redis connection options')
    if 'port' not in opts:
        raise Exception('Missing "port" in redis connection options')
    if 'db' not in opts:
        raise Exception('Missing "db" in redis connection options')
    host = opts['host']
    port = opts['port']
    db = opts['db']
    resource[AGE_KEY] = max_age
    r = redis.StrictRedis(host=host, port=port, db=db)
    r.set(uri, json.dumps(resource))
    del resource[AGE_KEY]
    return resource


def retrieve_resource(opts, uri, now):
    """ retrieve_resource will attempt to retrieve the resource stored
    in redis via the uri. If available and still cachable, the resource
    is returned.
    
    If no resource is found, None will be returned. If the resource is found,
    but is old, the resource is removed and None.
    """
    if 'host' not in opts:
        raise Exception('Missing "host" in redis connection options')
    if 'port' not in opts:
        raise Exception('Missing "port" in redis connection options')
    if 'db' not in opts:
        raise Exception('Missing "db" in redis connection options')
    host = opts['host']
    port = opts['port']
    db = opts['db']
    client = redis.StrictRedis(host=host, port=port, db=db)
    resource = client.get(uri)
    if not resource or resource and AGE_KEY not in resource:
        return None
    resource = json.loads(resource)
    max_age = int(resource[AGE_KEY])
    del resource[AGE_KEY]
    if max_age < now:
        client.delete(uri)
        return None
    return resource
