"""
amber_lib - a Python HTTP wrapper for interacting with the Amber Engine API
"""

from datetime import datetime, timedelta

from amber_lib.resources import send, BaseResource, create_affordance


_base_resources = {} # Keys are resource names. Values are affordances.
_expire_by = datetime.now() # Date/time of when the _base_resources needs to be refreshed


def _refresh_base_resources(cfg):
    """ Hit the API to retrieve top-level affordances for each resource.

    Send an OPTIONS request to the root path of the API to retrieve a list of
    all available resources and their generic affordances. Update the module
    variables `_base_resources` and `_expire_by`.
    """
    global _expire_by
    _expire_by = datetime.now() + timedelta(days=7)
    if cfg.debug:
        cfg.debug('%s: %s' % (
                'amber_lib.__init__._refresh_base_resources',
                'updating \'_expire_by\' to: %s' % _expire_by
            )
        )

    resp = send('options', cfg, '/')
    for key, val in resp.items():
        res = BaseResource()
        if key in _base_resources:
            res = _base_resources[key]
        for aff in val:
            method = aff.get('method', 'get')
            templated = aff.get('templated', False)
            name = aff.get('name', '')
            href = aff.get('href', '')


            res._add_affordance(name, create_affordance(cfg, method, href, templated))
        _base_resources[key] = res


def _get_base_resource(cfg, res):
    """Provide the specified resource. Update base resources if required.

    If no `_base_resources` exist, or they have been expired, hit the API to
    retrieve all available resources and their affordances. Then attempt to
    return the specified resource.
    """
    if not _base_resources or _expire_by < datetime.now():
        # Either no base resources, or past the expiration date. Refresh them.
        if cfg.debug:
            cfg.debug('%s: %s' % (
                    'amber_lib.__init__._get_base_resource',
                    'retrieving base resources from API'
                )
            )
        _refresh_base_resources(cfg)

    if res not in _base_resources:
        if cfg.debug:
            available_res = [k for k in _base_resources.keys()]
            cfg.debug('%s: %s' % (
                    'amber_lib.__init__.get_base_resource',
                    'current available resources: %s' % available_res
                )
            )
        raise AttributeError('API does not have resource \'%s\'' % res)

    return _base_resources[res]


class _Config(object):
    """Used to store settings required for communicating with the API.

    Instances of this class are passed around, providing necessary connection
    information, along with a couple misc options.
    """
    host = ''
    port = ''
    private = ''
    public = ''
    request_attempts = 3
    token = ''
    on_token_refresh = None
    debug = None # Can specify a function that takes 1 argument

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if isinstance(value, str):
                    value = value.strip()
                setattr(self, key, value)
            else:
                raise AttributeError(key)


class Context(object):
    """Interface for using base API resources, and stores required settings."""
    def __init__(self, **kwargs):
        self.config = _Config(**kwargs)

    def __getattr__(self, key):
        return _get_base_resource(self.config, key)
