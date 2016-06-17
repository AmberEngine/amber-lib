import amber_lib.client as client
import amber_lib.models.components as components
import amber_lib.models.primaries as primaries
import amber_lib.models.product as product


class Connection(object):
    """ Connection is used to instantiate models with a specified Context.
    """

    def __init__(self, settings):
        """ Initialize a new Connection instance, providing an instantiated
        instance of the Context class.
        """
        self.context = settings
        self.use_components = False

    def __enter__(self):
        """ Allows the use of the with-keyword for ease of use.
        """
        return self

    def __exit__(self, exception_type, exception_val, trace):
        """ Allows the use of the with-keyword for ease of use. This is a no-op
        method.
        """
        pass

    def __getattr__(self, attr):
        """ Try to retrieve the specified attribute from the various model
        modules. If the attribute is a component, it must can only be accessed
        first through the `components` attribute key.
        """
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

    def ping(self):
        """ Attempt to ping the API server using the current Connection's
        context.
        """
        client.send(client.GET, self.context, '', {})
