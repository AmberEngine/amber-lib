import json

from amber_lib import client


class Model(object):
    """ Model is a base class which contains all the methods requires for
    the various CRUD methods on database entries, querying, and managing
    database entries.
    """
    _ctx = None
    _links = {}
    _pk = "id"
    _resource = 'models'

    def __init__(self, context):
        """ Initialize a new instance of the Model, saving the current context
        internally.
        """
        self._ctx = context

    def __getattr__(self, attr):
        """ This magic method is called when access to an attribute which
        does not exist occurrs.
        """
        raise AttributeError(
            '"%s" does not have: %s' % (self.__class__.__name__, attr)
        )

    def __getattribute__(self, attr):
        """ This magic method is called whenever access to an attribute is
        attempted, even if that attribute does not exist.
        """
        obj_attr = object.__getattribute__(self, attr)
        if attr.startswith('_') or hasattr(obj_attr, '__call__'):
            return obj_attr
        return obj_attr.value

    def __setattr__(self, attr, val):
        """ If the attribute exists, set it. Otherwise raise an exception."""
        if attr.startswith('_'):
            self.__dict__[attr] = val
            return
        elif attr in self.__dict__:
            self.__dict__[attr].__set__(self, val)
            return
        else:
            prop = find(self, attr)
            if not prop:
                raise AttributeError(
                    "[%s] %s:%s" % (self.__class__, attr, val)
                )

            self.__dict__[attr] = Property(prop.kind, prop.is_list)
            setattr(self, attr, val)

    def ctx(self):
        """ Retrieve the context of the model.
        """
        return self._ctx

    def delete(self, id_=None):
        """ Delete the current model, delete the model as specified by ID, or
        error out, depending on the weather conditions.
        """
        if self.is_valid():
            if id_ is not None:
                raise ValueError(
                    'Cannot delete using an already instantiated model. >:('
                )
            client.send(
                client.DELETE,
                self.ctx(),
                self.endpoint(),
                None
            )
        elif id_ is not None:
            setattr(self, self._pk, id_)
            client.send(
                client.DELETE,
                self.ctx(),
                self.endpoint(),
                None
            )
        else:
            raise ValueError

        self.__dict__ = {}
        return self

    def endpoint(self):
        """ Generate and retrieve an API URL endpoint for the current model.
        """
        loc = "/%s" % self._resource

        if not self.is_valid():
            return loc

        if isinstance(self.pk(), int) and self.pk() > 0:
            return loc + "/%d" % self.pk()
        raise TypeError

    def from_dict(self, dict_):
        """ Update the internal dictionary for the instance using the
        key-value pairs contained within the provided dictionary.
        """
        def explode_dict(obj, exp_dict):
            for key, val in exp_dict.items():
                attr = object.__getattribute__(obj, key)

                if isinstance(val, dict):
                    if not isinstance(attr, dict):
                        inst = None
                        if isinstance(attr.kind, tuple):
                            for kind in attr.kind:
                                if isinstance(val, kind):
                                    inst = kind(obj.ctx())
                        else:
                            inst = attr.kind(obj.ctx())
                        # Try to fill the new instance with data from the old
                        # instance so we don't lose data that isn't included
                        # in the val
                        orig = getattr(obj, key)
                        if orig:
                            inst.update(orig.to_dict())
                        val = explode_dict(inst, val)
                elif isinstance(val, list):
                    list_ = []
                    for el in val:
                        if isinstance(el, dict):
                            inst = attr.kind(obj.ctx())
                            el = explode_dict(inst, el)
                        list_.append(el)
                    val = list_
                setattr(obj, key, val)
            return obj
        return explode_dict(self, dict_)

    def from_json(self, json_):
        """ Update the internal dictionary for the instance using the
        key-value pairs stored within the provided JSON string.
        """
        dict_ = json.loads(json_)
        return self.from_dict(dict_)

    def pk(self):
        """ Retrieve the primary key for the current model.
        """
        return getattr(self, self._pk)

    def query(self, filtering=None, batch_size=500, offset=0, **kwargs):
        """ Retrieve a collection of instances of the model, using the
        URI params from the keyword arguments.
        """
        # TODO: Limit the total returned results.
        # TODO: Accept fields to pass on to client.send as a kwarg
        payload = client.send(
            client.GET,
            self._ctx,
            self.endpoint(),
            {"filtering": filtering.to_dict()} if filtering else None,
            limit=batch_size,
            offset=offset,
            **kwargs
        )

        collection = client.Container(
            payload,
            self.__class__,
            self._ctx,
            offset
        )

        return collection

    def set_relation(self, bool_, obj):
        """ Create or remove a relation between the current model and a
        different model.
        """
        payload = client.send(
            client.POST if bool_ is True else client.DELETE_,
            self.ctx(),
            "/relations",
            **{
                self._resource: self.pk(),
                obj._resource: obj.pk()
            }
        )

    def relate(self, obj):
        """ Create a relation between this object and another.
        """
        self.set_relation(True, obj)

    def retrieve(self, id_=None):
        """ Retrieve the data for a database entry constrained by the
        specified ID, and udpate the current instance using the retrieved
        data.
        """
        if id_ is not None:
            setattr(self, self._pk, id_)

        payload = client.send(
            client.GET,
            self.ctx(),
            self.endpoint(),
            None,
        )
        self.from_dict(payload)

        return self

    def is_valid(self):
        """ Determine if the current model is valid, based on the contents
        of its primary key.
        """
        return hasattr(self, self._pk) and \
            getattr(self, self._pk) is not None and \
            int(getattr(self, self._pk)) > 0

    def refresh(self):
        """ If the current entity is valid, update it by retrieve it's own
        data and perform an internal update.
        """
        if self.is_valid():
            self.retrieve(self.pk())
        else:
            raise Exception

    def save(self, data=None):
        """ Save the current state of the model into the database, either
        creating a new entry or updating an existing database entry. It
        is dependent on whether a valid ID is present (which is required
        for updates).
        """
        if data is not None:
            self.update(data)

        if self.is_valid():
            returned_dict = client.send(
                client.PUT,
                self.ctx(),
                self.endpoint(),
                self.to_dict()
            )
        else:
            returned_dict = client.send(
                client.POST,
                self.ctx(),
                self.endpoint(),
                self.to_dict()
            )

        self.update(returned_dict)
        return self

    def to_dict(self):
        """ Retrieve a dictionary version of the model.
        """
        def collapse_dict(obj):
            dict_ = {}
            for key in dir(obj):
                value = getattr(obj, key)
                if key.startswith('_'):
                    continue
                if hasattr(value, '__call__'):
                    continue
                item = value
                if isinstance(item, Model):
                    dict_[key] = collapse_dict(item)
                elif isinstance(item, list):
                    list_ = []
                    for el in item:
                        if isinstance(el, Model):
                            list_.append(collapse_dict(el))
                        else:
                            list_.append(el)
                    dict_[key] = list_
                else:
                    prop = find(obj, key)
                    if prop is not None:
                        if isinstance(prop.kind, type) and \
                                issubclass(prop.kind, Model):
                            continue
                    dict_[key] = item
            return dict_
        return collapse_dict(self)

    def to_json(self):
        """ Retrieve the model as a JSON object string, containing
        key-value pairs for the internal class data.
        """
        return json.dumps(self.to_dict())

    def unrelate(self, obj):
        """ Unrelate this object and another object.
        """
        self.set_relation(False, obj)

    def update(self, data):
        """ Update the internal data of the class instance using either
        a string JSON object or a dictionary.
        """
        if isinstance(data, str):
            return self.from_json(data)
        elif isinstance(data, dict):
            return self.from_dict(data)
        else:
            raise TypeError

    def form_schema(self):
        """ Retrieve the Schema for the """
        endpoint = "/form_schemas/%s" % self._resource
        response = client.send(client.GET, self.ctx(), endpoint, {})
        return response


class Property(object):
    """ Enable enforcing static-typing in the dynamic langaugage Python. This
    can't be a bad idea, right? Hurray!
    """

    def __init__(self, kind, is_list=False):
        """ Initialize a new Property, specifying the class and whether
        it should be a list of things or not.
        """
        self.kind = kind
        self.is_list = is_list
        self.value = None
        if is_list:
            self.value = []

    def __set__(self, obj, value):
        """ When attempting to set this Property, as an attribute, to a new
        value, the new value must first match the rules of the instantiated
        Property. Otherwise an exception is raised.
        """
        if type(value).__name__ == 'unicode':
            value = value.encode('utf-8')
        if value is None or (isinstance(value, str) and not value and \
                not isinstance(self.kind, str)):
            self.value = None
        elif self.is_list is True:
            if not isinstance(value, list):
                raise TypeError('Value: \'%s\' is not a list' % value)
            else:
                list_ = []
                for val in value:

                    if type(val).__name__ == 'unicode':
                        val = val.encode('utf-8')
                    if isinstance(val, self.kind) is False:
                        if self.kind == int and isinstance(val, str) and val.isdigit():
                            val = int(val)
                        else:
                            raise TypeError(
                                'Type: \'%s\' is not \'%s\'' % (
                                    type(val),
                                    self.kind
                                )
                            )
                    list_.append(val)
                self.value = list_
        elif isinstance(value, self.kind):
            self.value = value
        elif isinstance(value, int) and self.kind == float:
            self.value = float(value)
        elif isinstance(value, float) and self.kind == int:
            self.value = int(value)
        elif self.kind == str:
            self.value = value
        elif self.kind == int and isinstance(value, str) and value.isdigit():
            self.value = int(value)
        else:
            raise TypeError(
                'Type: \'%s\' for \'%s\' is not \'%s\'' % (type(value), value, self.kind)
            )

def find(obj, key):
    if key in obj.__dict__:
        return obj.__dict__[key]
    if key in obj.__class__.__dict__:
        return obj.__class__.__dict__[key]

    for parent in obj.__class__.__bases__:
        if issubclass(parent, Model):
            result = find(parent, key)
            if result:
                return result
    return None


def resource(endpoint, pk="id"):
    """ This is a decorator for specifying a endpoint and what attribute
    stores the primary key for a model.
    """
    def set_resource(obj):
        obj._resource = endpoint
        return obj
    return set_resource
