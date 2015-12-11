import amber_lib.models.primaries as primaries
import amber_lib.models.product as product
import amber_lib.models.components as components


class Connection(object):
    def __init__(self, settings):
        self.context = settings

    def __getattr__(self, attr):
        look_in = [primaries, product, components]
        for module in look_in:
            if hasattr(module, attr):
                return getattr(module, attr)(self.context)
        raise AttributeError

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        pass


