import json


class Model(object):
    _ctx = None

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
        for key, val in dict_.iteritems():
            if key not in self.__dict__.keys():
                raise Exception("That key dont exist, yo!")
            else:
                self.__dict__[key] = val

        return self

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
            returnedDict = amberlib.Put(self.ctx, self.__class__, self.toDict(), id=self.id)
        else:
            returnedDict = amberlib.Post(self.ctx, self.__class__, self.toDict())

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



class Component(Model):
    def save(self, data=None):
        pass
