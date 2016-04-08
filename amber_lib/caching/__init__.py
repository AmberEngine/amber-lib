#Embedded file name: /Users/curtislagraff/.virtualenvs/amber-lib/amber-lib/amber_lib/caching/__init__.py
import time
from amber_lib.caching import redis_driver
AVAILABLE_SYSTEMS = {'redis': redis_driver,
 'mongo': None}

def cache_response(ctx, response, age):
    if not hasattr(ctx, 'cache'):
        raise Exception('Caching requires cache connection string')
    conn_string = ctx.cache
    options = dict((entry.strip().split('=') for entry in conn_string.split(';')))
    system_name = options.get('system', None)
    if system_name not in AVAILABLE_SYSTEMS:
        raise Exception('System: "%s" not in avaliable systems: "%s"' % (system, AVAILABLE_SYSTEMS.keys()))
    system = AVAILABLE_SYSTEMS[system_name]
    if '_links' in response and 'self' in response['_links']:
        link = response['_links']['self']['href']
        max_age = int(time.time()) + age
        system.cache_resource(options, link, response, max_age)


def get_cache(ctx, uri):
    if not hasattr(ctx, 'cache'):
        raise Exception('Caching requires cache connection string')
    conn_string = ctx.cache
    options = dict((entry.strip().split('=') for entry in conn_string.split(';')))
    system_name = options.get('system', None)
    if system_name not in AVAILABLE_SYSTEMS:
        raise Exception('System: "%s" not in avaliable systems: "%s"' % (system, AVAILABLE_SYSTEMS.keys()))
    system = AVAILABLE_SYSTEMS[system_name]
    return system.retrieve_resource(options, uri, int(time.time()))
