from datetime import datetime, timedelta

from amber_lib.resources import send, BaseResource, create_affordance

_base_resources = {}
_expire_by = datetime.now()


def _refresh_base_resources(cfg):
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
    if not _base_resources or _expire_by < datetime.now():
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
        raise AttributeError('API has not resource \'%s\'')

    return _base_resources[res]


class _Config(object):
    host = ''
    port = ''
    private = ''
    public = ''
    request_attempts = 3
    token = ''
    on_token_refresh = None
    debug = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if isinstance(value, str):
                    value = value.strip()
                setattr(self, key, value)
            else:
                raise AttributeError(key)


class Context(object):
    def __init__(self, **kwargs):
        self.config = _Config(**kwargs)

    def __getattr__(self, key):
        return _get_base_resource(self.config, key)
