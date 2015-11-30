import json


class Model(object):
    _ctx = None
    attributes = {}

    def __init__(self, context):
        """ Initialize a new instance of the Model, saving the current context
        internally.
        """
        self._ctx = context

    def __getattr__(self, attr):
        """ If the desired attribute exists, return the current value that it
        is storing internally.
        """
        if attr in self.attributes:
            return self.attributes[attr].get()
        else:
            raise Exception('NOPE NOPE NOPE!')

    def __setattr__(self, attr, val):
        """ If the desired attribute exists, set its internal value using
        the set method to that of the specified value.
        """
        if attr in self.attributes:
            self.attributes[attr].set(val)
        else:
            raise Exception('nope!')

    def all(self, limit=500, offset=0):
        """ Retrieve a collection of instances of the model, using the
        URI params from the keyword arguments.
        """
        payload = amberlib.Get(self.ctx, self.toDict(), limit=500, offset=0)
        collection = amberlib.Collection(json.loads(payload))

        return collection

    def fromDict(self, dict_):
        """ Update the internal dictionary for the instance using the
        key-value pairs contained within the provided dictionary.
        """
        def explodeDict(obj, dict_):
            for key, val in dict_.items():
                if key not in obj.attributes:
                    raise Exception("yo! That dont work!")

                if isinstance(val, [dict]):
                    dict_ = val
                    inst = getattr(amberlib.models.components, key)(self._ctx)

                obj.attributes[key].set(val)
            return obj

        return explodeDict(self, dict_)

    def fromJSON(self, json):
        """ Update the internal dictionary for the instance using the
        key-value pairs stored within the provided JSON string.
        """
        dict_ = json.loads(json)
        return self.fromDict(dict_)

    def save(self, data=None):
        """ Save the current state of the model into the database, either
        creating a new entry or updating an existing database entry. It
        is dependent on whether a valid ID is present (which is required
        for updates).
        """
        if data is not None:
            self.update(data)

        if isinstance(self.id, int) and self.id > 0:
            returnedDict = amberlib.Put(
                self.ctx,
                self.__class__,
                self.toDict(),
                id=self.id
            )
        else:
            returnedDict = amberlib.Post(
                self.ctx,
                self.__class__,
                self.toDict()
            )

        self.update(returned)
        return self

    def toDict(self):
        """ Retrieve a dictionary version of the model.
        """
        dictionary = {}

        for key, val in self.__dict__.iteritems():
            if key.startswith("_"):
                continue
            if isinstance(val, Model):
                val = val.toDict()

            dictionary[key] = val

        return dictionary

    def toJSON(self):
        """ Retrieve the model as a JSON object string, containing
        key-value pairs for the internal class data.
        """
        return json.dumps(self.toDict())

    def update(self, data):
        """ Update the internal data of the class instance using either
        a string JSON object or a dictionary.
        """
        if isinstance(data, str):
            return self.fromJSON(data)
        elif isinstance(data, dict):
            return self.fromDict(data)
        else:
            raise Exception("shit aint right")

    def retrieve(self, id_):
        """ Retrieve the data for a database entry constrained by the
        specified ID, and udpate the current instance using the retrieved
        data.
        """
        payload = amberlib.Get(self.ctx, self.__class__, self.toDict(), id=id_)
        self.fromJSON(payload)

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
    attributes = {}

    def __init__(self, *args, **kwargs):
        self.attributes["component_data_id"] = Property(int)
        self.attributes["product_id"] = Property(int)
        self.attributes["parent_component_id"] = Property(int)
        self.attributes["parent_table_name"] = Property(str)

        Model.__init__(self, *args, **kwargs)

    def save(self, data=None):
        pass
