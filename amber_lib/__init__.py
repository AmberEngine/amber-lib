"""
amber_lib - a Python HTTP wrapper for interacting with the Amber Engine API
"""

from datetime import datetime, timedelta

from amber_lib.resources import send, BaseResource, create_affordance


class _Config(object):
    """Used to store settings required for communicating with the API.

    Instances of this class are passed around, providing necessary connection
    information, along with a couple misc options.
    """
    def __init__(self, **kwargs):
        self.host = ''
        self.port = ''
        self.private = ''
        self.public = ''
        self.request_attempts = 3
        self.token = ''
        self.on_token_refresh = None
        self.debug = None # Can specify a function that takes 1 argument

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
        self.base_resources = {}
        self._expire_by = datetime.now()

    def __getattr__(self, key):
        is_expired = self._expire_by < datetime.now()

        if not self.base_resources or is_expired or key not in self.base_resources:
            # Either no base resources, or past the expiration date. Refresh them.
            if self.config.debug:
                self.config.debug('%s: %s' % (
                        'amber_lib.__init__._get_base_resource',
                        'retrieving base resources from API'
                    )
                )
            self.refresh_base_resources()

        if key not in self.base_resources:
            if self.config.debug:
                available_res = [k for k in _base_resources.keys()]
                self.config.debug('%s: %s' % (
                        'amber_lib.__init__.get_base_resource',
                        'current available resources: %s' % available_res
                    )
                )
            raise AttributeError('No API resource named: "%s"' % key)

        return self.base_resources[key]

    def refresh_base_resources(self):
        """ Hit the API to retrieve top-level affordances for each resource.

        Send an OPTIONS request to the root path of the API to retrieve a list of
        all available resources and their generic affordances. Update the module
        variables `_base_resources` and `_expire_by`.
        """
        self._expire_by = datetime.now() + timedelta(days=7)
        if self.config.debug:
            self.config.debug('%s: %s' % (
                    'amber_lib.__init__._refresh_base_resources',
                    'updating "_expire_by" to: %s' % self._expire_by
                )
            )

        resp = send('options', self.config, '/')
        for key, val in resp.items():
            res = BaseResource()
            for name in val:
                aff = val[name]
                method = aff.get('method', 'get')
                templated = aff.get('templated', False)
                name = aff.get('name', '')
                href = aff.get('href', '')


                res._add_affordance(name, create_affordance(self.config, method, href, templated))
            self.base_resources[key] = res
