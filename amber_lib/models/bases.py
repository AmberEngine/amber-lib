import copy
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

    @property
    def ctx(self):
        return self._ctx

    def __getattr__(self, attr):
        raise AttributeError(
            '"%s" does not have: %s' % (self.__class__.__name__, attr)
        )

    def __setattr__(self, attr, val):
        """ If the attribute exists, set it. Otherwise raise an exception."""
        if attr.startswith('_'):
            self.__dict__[attr] = val
        else:
            property_ = getattr(self, attr)
            if attr not in self.__dict__:
                self.__dict__[attr] = Property(property_.kind, property_.is_list)
            self.__dict__[attr].set(val)
        #getattr(self, attr).set(val)

    def query(self, batch_size=500, offset=0):
        """ Retrieve a collection of instances of the model, using the
        URI params from the keyword arguments.
        """
        # TODO: Limit the total returned results.
        # TODO: Accept fields to pass on to client.send as a kwarg
        payload = client.send(
            client.GET,
            self._ctx,
            self.endpoint(),
            None,
            limit=batch_size,
            offset=offset
        )

        collection = client.Container(
            payload,
            self.__class__,
            self._ctx,
            offset
        )

        return collection

    def endpoint(self):
        loc = "/%ss" % self.__class__.__name__.lower()

        id_val = 0
        if hasattr(self, "id") is False or self.id is None:
            return loc

        if isinstance(self.id, int) and self.id > 0:
            return loc + "/%d" % self.id
        elif isinstance(self.id, Property):
            if self.id.value > 0:
                return loc + "/%d" % self.id.value
            else:
                return loc

        raise TypeError

    def from_dict(self, dict_):
        """ Update the internal dictionary for the instance using the
        key-value pairs contained within the provided dictionary.
        """
        def explode_dict(obj, exp_dict):
            for key, val in exp_dict.items():
                if key.startswith('_'):
                    obj.__dict__[key] = val
                    continue
                is_list = isinstance(val, list)
                attr = getattr(obj, key)

                if isinstance(val, dict):
                    if not isinstance(attr, dict):
                        inst = attr.kind(obj.ctx)
                        val = explode_dict(inst, val)
                elif isinstance(val, list):
                    list_ = []
                    for el in val:
                        if isinstance(el, dict):
                            inst = attr.kind(obj.ctx)
                            el = explode_dict(inst, el)
                        list_.append(el)
                    val = list_
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
            returned_dict = client.send(
                client.PUT,
                self.ctx,
                self.endpoint(),
                self.to_dict()
            )
        else:
            returned_dict = client.send(
                client.POST,
                self.ctx,
                self.endpoint(),
                self.to_dict()
            )
        #self = self.__class__(self.ctx)
        self.update(returned_dict)

        return self

    def to_dict(self):
        """ Retrieve a dictionary version of the model.
        """
        def collapse_dict(obj):
            dict_ = {}

            for key, value in obj.__dict__.items():
                if key.startswith('_'):
                    continue
                    # self.__dict__[key] = value
                item = value.get()
                if isinstance(item, Model):
                    dict_[key] = collapse_dict(item)
                elif isinstance(item, list):
                    list_ = []
                    for el in item:
                        list_.append(collapse_dict(el))
                    dict_[key] = list_
                else:
                    dict_[key] = item
            return dict_
        return collapse_dict(self)

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

    def __getattr__(self, key):
        if hasattr(self.value, key):
            return getattr(self.value, key)
        raise AttributeError

    def __setattr__(self, attr, value):
        if attr not in ['kind', 'is_list', 'value']:
            setattr(self.value, attr, value)
        else:
            self.__dict__[attr] = value

    def get(self):
        return self.value

    def set(self, value):
        if value is None:
            self.value = None
        elif self.is_list is True:
            if not isinstance(value, list):
                raise TypeError('Value: \'%s\' is not a list' % value)
            else:
                for val in value:
                    if isinstance(val, self.kind) is False:
                        raise TypeError('Type: \'%s\' is not \'%s\'' % (type(val), self.kind))
                    self.value = value
        elif isinstance(value, self.kind):
            self.value = value
        elif isinstance(value, unicode) and self.kind == str:
            self.value = value.encode('utf-8')
        elif isinstance(value, int) and self.kind == float:
            self.value = float(value)
        else:
            raise TypeError('Type: \'%s\' is not \'%s\'' % (type(value), self.kind))


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
