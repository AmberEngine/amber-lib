import amber_lib.models.primaries as primaries
import amber_lib.models.product as product
import amber_lib.models.components as components


class Connection(object):
    def __init__(self, settings):
        self.context = settings
        self.use_components = False

    def __getattr__(self, attr):
        if attr == 'components':
            self.use_components = True
            return self

        if self.use_components:
            if hasattr(components, attr):
                self.use_components = False
                return getattr(components, attr)(self.context)
        else:
            look_in = [primaries, product]
            for module in look_in:
                if hasattr(module, attr):
                    return getattr(module, attr)(self.context)
        raise AttributeError

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        pass


