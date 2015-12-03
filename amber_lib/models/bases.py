import json

from amber_lib import client


class Model(object):
    _ctx = None
    _links = {}

    def __init__(self, context):
        """ Initialize a new instance of the Model, saving the current context
        internally.
        """
        self._ctx = context

    def __getattr__(self, attr):
        raise AttributeError('"%s" does not have: %s' % (self.__class__.__name__, attr))

    def __setattr__(self, attr, val):
        """ If the attribute exists, set it. Otherwise raise an exception."""
        getattr(self, attr)
        self.__dict__[attr] = val

    def all(self, limit=500, offset=0):
        """ Retrieve a collection of instances of the model, using the
        URI params from the keyword arguments.
        """
        payload = client.send(
            client.GET,
            self.ctx,
            self.endpoint(),
            None,
            limit=500,
            offset=0
        )

        collection = client.Collection(
            json.loads(payload),
            self.__class__,
            self._ctx,
        )

        return collection

    def endpoint(self):
        loc = self.__class__.__name__

        if hasattr(self, "id"):
            loc += "/%d" % self.id
        return loc

    def from_dict(self, dict_):
        """ Update the internal dictionary for the instance using the
        key-value pairs contained within the provided dictionary.
        """
        def explode_dict(obj, dict_):
            for key, val in dict_.items():
                # Are we working with a dict?
                if isinstance(val, dict):
                    # Capitailize the Key.
                    # Create new instance with current context.
                    attr = getattr(self, key)
                    if not isinstance(attr, dict):
                        inst = getattr(self, key).kind(self._ctx)
                        val = explode_dict(inst, val)
                elif isinstance(val, list):
                    pass

                setattr(obj, key, val)
            return obj
        return explode_dict(self, dict_)

    def from_json(self, json):
        """ Update the internal dictionary for the instance using the
        key-value pairs stored within the provided JSON string.
        """
        dict_ = json.loads(json)
        return self.from_dict(dict_)

    def save(self, data=None):
        """ Save the current state of the model into the database, either
        creating a new entry or updating an existing database entry. It
        is dependent on whether a valid ID is present (which is required
        for updates).
        """
        if data is not None:
            self.update(data)

        if hasattr(self, "id") and self.id > 0:
            returnedDict = amberlib.Put(
                self.ctx,
                self.endpoint(),
                self.to_dict()
            )
        else:
            returnedDict = amberlib.Post(
                self.ctx,
                self.endpoint(),
                self.to_dict()
            )

        self.update(returned)
        return self

    def to_dict(self):
        """ Retrieve a dictionary version of the model.
        """
        dictionary = {}

        for key, val in self.__dict__.iteritems():
            if key.startswith("_"):
                continue
            if isinstance(val, Model):
                val = val.to_dict()

            dictionary[key] = val

        return dictionary

    def to_json(self):
        """ Retrieve the model as a JSON object string, containing
        key-value pairs for the internal class data.
        """
        return json.dumps(self.to_dict())

    def update(self, data):
        """ Update the internal data of the class instance using either
        a string JSON object or a dictionary.
        """
        if isinstance(data, str):
            return self.from_json(data)
        elif isinstance(data, dict):
            return self.from_dict(data)
        else:
            raise Exception("shit aint right")

    def retrieve(self, id_):
        """ Retrieve the data for a database entry constrained by the
        specified ID, and udpate the current instance using the retrieved
        data.
        """
        payload = amber_lib.Get(self.ctx, self.endpoint(), self.to_dict(), id=id_)
        self.from_json(payload)

        return self


class Property:
    def __init__(self, kind, is_list=False):
        self.kind = kind
        self.is_list = is_list
        self.value = None

    def get(self):
        return self.value

    def set(self, value):
        if self.is_list is True:
            if not isinstance(value, list):
                raise Exception("Expecting a list!")
            for val in value:
                self.set(val)
        elif isinstance(value, self.kind):
            self.value = value
        else:
            raise Exception('wrong type!')


class Component(Model):
    component_data_id = Property(int)
    product_id = Property(int)
    parent_component_id = Property(int)
    parent_table_name = Property(str)

    def save(self, data=None):
        if data is not None:
            self.update(data)

        if isinstance(self.component_data_id, int) and self.component_data_id > 0:
            returned_dict = amber_lib.Put(
                self.ctx,
                self.__class__,
                self.to_dict(),
                id=self.component_data_id
            )
        else:
            returned_dict = amber_lib.Post(
                self.ctx,
                self.__class__,
                self.to_dict()
            )

        self.update(returned_dict)
        return self
