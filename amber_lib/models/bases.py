import json, random, string

from amber_lib import client, errors, query




def randStr(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

def randInt():
    return int(random.random()*100000) + 1

def randWords(amt):
    words = []
    for i in range(amt):
        words.append(
            randStr(
                int(
                    random.random()*7
                ) + 1
            )
        )
    return " ".join(words)



class Model(object):
    """ Model is a base class which contains all the methods requires for
    the various CRUD methods on database entries, querying, and managing
    database entries.
    """
    _ctx = None
    _links = {}
    _pk = 'id'
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
            # Can we find the attribute on a parent class? Then set it in the
            # local dictionary. Otherwise, raise an exception.
            prop = find(self, attr)
            if not prop:
                raise AttributeError(
                    '[%s] %s:%s' % (self.__class__, attr, val)
                )

            self.__dict__[attr] = Property(prop.kind, prop.is_list)
            setattr(self, attr, val)

    def _randomize(self):
        for key in self.__class__.__dict__:
            self.__dict__[key] = self.__class__.__dict__[key]
            prop = self.__dict__[key]
            if not isinstance(prop, Property):
                continue
            if not prop.is_list:
                if prop.kind == int:
                    setattr(self, key, randInt())
                elif prop.kind == str:
                    setattr(self, key, randStr(4 + (randInt() % 10)))
                elif prop.kind == bool:
                    setattr(self, key, 2 == random.random()*2)
                elif hasattr(prop.kind, '_randomize'):
                    new_instance = prop.kind(self.ctx())
                    new_instance._randomize()
                    setattr(self, key, new_instance)
            else:
                list_ = []
                for i in range((randInt() % 10) + 2):
                    if prop.kind == int:
                        list_.append(randInt())
                    elif prop.kind == str:
                        list_.append(randStr(4 + (randInt() % 10)))
                    elif prop.kind == bool:
                        list_.append(2 == random.random()*2)
                    elif hasattr(prop.kind, '_randomize'):
                        new_instance = prop.kind(self.ctx())
                        new_instance._randomize()
                        list_.append(new_instance)
                setattr(self, key, list_)


    def clear(self):
        """ clear will remove all public attributes from the model by
        deleting the respective entries in the object's internal dictionary.
        Private and callable attributes are not removed.
        """
        dict_ = self.__dict__.copy()
        for key in dict_:
            if key.startswith('_'):
                continue
            if hasattr(dict_[key], '__call__'):
                continue
            del self.__dict__[key]

    def ctx(self):
        """ Retrieve the context of the model.
        """
        return self._ctx

    def delete(self, id_=None):
        """ Delete the current model, delete the model as specified by ID, or
        error out, depending on the weather conditions.
        """
        if self.is_valid():
            # Delete current model
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
            # Delete model by passed id_
            setattr(self, self._pk, id_)
            client.send(
                client.DELETE,
                self.ctx(),
                self.endpoint(),
                None
            )
        else:
            raise ValueError

        self.__dict__.clear()
        return self

    def mock_delete(self, id_=None):
        if self.is_valid() and id_ is not None:
            raise ValueError('Cannot delete using an already instantiated model.')
        self.__dict__.clear()
        return self


    def endpoint(self):
        """ Generate and retrieve an API URL endpoint for the current model.
        """
        loc = '/%s' % self._resource

        if not self.is_valid():
            return loc

        if isinstance(self.pk(), int) and self.pk() > 0:
            return loc + '/%d' % self.pk()
        raise TypeError

    def form_schema(self):
        """ Retrieve the Schema for the """
        endpoint = '/form_schemas/%s' % self._resource
        response = client.send(client.GET, self.ctx(), endpoint, {})
        return response

    def from_dict(self, dict_):
        """ Update the internal dictionary for the instance using the
        key-value pairs contained within the provided dictionary.
        """
        def explode_dict(obj, exp_dict):
            for key, val in exp_dict.items():
                attr = object.__getattribute__(obj, key)

                if isinstance(val, dict):
                    if not isinstance(attr, dict):
                        inst = attr.kind(obj.ctx())
                        # Try to fill the new instance with data from the old
                        # instance so we don't lose data that isn't included
                        # in the val
                        orig = getattr(obj, key)
                        if orig:
                            inst.update(orig.to_dict())
                        val = inst.from_dict(val)
                elif isinstance(val, list):
                    list_ = []
                    for el in val:
                        if isinstance(el, dict):
                            inst = attr.kind(obj.ctx())
                            el = inst.from_dict(el)
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

    def is_valid(self):
        """ Determine if the current model is valid, based on the contents
        of its primary key.
        """
        if not hasattr(self, self._pk):
            return False
        if getattr(self, self._pk) is None:
            return False
        try:
            return int(getattr(self, self._pk)) > 0
        except ValueError:
            return False

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
        if filtering and isinstance(filtering, query.Predicate):
            filtering = query.WhereItem(pred=filtering)
        try:
            payload = client.send(
                client.GET,
                self._ctx,
                self.endpoint(),
                {'filtering': filtering.to_dict()} if filtering else None,
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
        except errors.NotFound:
            collection = client.Container({}, self.__class__, self._ctx, 0)

        return collection

    def mock_query(self, filtering=None, batch_size=500, offset=0, amount=10, **kwargs):
        import copy
        array = []
        for i in range(amount):
            t = copy.deepcopy(self)
            t._randomize()
            array.append(t)
        return array

    def relate(self, obj, refresh=True, **kwargs):
        """ Create a relation between this object and another.
        """
        self.set_relation(True, obj, refresh=refresh, **kwargs)

    def mock_relate(self, obj, refresh=True):
        self.mock_set_relation(True, obj, refresh=refresh)

    def relate_many(self, objs, refresh=True, **kwargs):
        """ Create a relation between this object and another.
        """
        self.set_relation_multiple(True, objs, refresh=refresh, **kwargs)

    def mock_relate_many(self, objs, refresh=True):
        self.mock_set_relation(True, objs, refresh=refresh)

    def retrieve(self, id_=None, **kwargs):
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
            **kwargs
        )
        self.clear()
        self.from_dict(payload)

        return self

    def mock_retrieve(self, id_=None):
        self.clear()
        self._randomize()
        return self

    def refresh(self):
        """ If the current entity is valid, update it by retrieve it's own
        data and perform an internal update.
        """
        if self.is_valid():
            self.retrieve(self.pk())
        else:
            raise Exception

    def mock_refresh(self):
        if self.is_valid():
            self.mock_retrieve(self.pk())
        else:
            raise Exception


    def partial_save(self, data=None, **kwargs):
        """ Save the current state of the model into the database, either
        creating a new entry or updating an existing database entry. It
        is dependent on whether a valid ID is present (which is required
        for updates).
        """
        self_dict = self.to_dict()
        if 'guid' in self_dict:
            kwargs['guid'] = self_dict['guid']

        if data is not None:
            self.update(data)

        if self.is_valid():
            returned_dict = client.send(
                client.PATCH,
                self.ctx(),
                self.endpoint(),
                self_dict,
                **kwargs
            )
        else:
            raise Exception("Cannot perform partial save without valid primary key")

        self.clear()
        self.update(returned_dict)
        return self


    def save(self, data=None, **kwargs):
        """ Save the current state of the model into the database, either
        creating a new entry or updating an existing database entry. It
        is dependent on whether a valid ID is present (which is required
        for updates).
        """
        self_dict = self.to_dict()
        if 'guid' in self_dict:
            kwargs['guid'] = self_dict['guid']

        if data is not None:
            self.update(data)

        if self.is_valid():
            returned_dict = client.send(
                client.PUT,
                self.ctx(),
                self.endpoint(),
                self_dict,
                **kwargs
            )
        else:
            returned_dict = client.send(
                client.POST,
                self.ctx(),
                self.endpoint(),
                self_dict,
                **kwargs
            )

        self.clear()
        self.update(returned_dict)
        return self

    def mock_save(data=None, **kwargs):
        self.clear()
        self._randomize()
        return self

    def set_relation(self, bool_, obj, refresh=True, **kwargs):
        """ Create or remove a relation between the current model and a
        different model.
        """
        self.save()
        res1 = self._resource
        res2 = obj._resource

        if res2 == res1:
            res2 = "other_%s" % res1

        kwargs[res1] = self.pk()
        kwargs[res2] = obj.pk()

        payload = client.send(
            client.POST if bool_ is True else client.DELETE,
            self.ctx(),
            '/relations',
            **kwargs
        )
        # Dear Future Dev, if you're wondering why changes are disappearing
        # when relate/unrelate calls are made then this line is why, but
        # without it then relate/unrelate changes disappear on save calls.
        if refresh:
            obj.refresh()
            self.refresh()

    def mock_set_relation(self, bool_, obj, refresh=True):
        self.mock_save()

    def set_relation_multiple(self, bool_, objs, refresh=True):
        """ Create or remove a relation between the current model and a
        different model.
        """
        self.save()
        res1 = self._resource
        if len(objs) == 0:
            raise Exception("Must provide at least one object to relate to.")
        if not isinstance(objs, (list, client.Container)):
            raise Exception("Must provide a list of objects to relate to.")

        res2 = objs[0]._resource

        if res2 == res1:
            res2 = "other_%s" % res1

        payload = client.send(
            client.POST if bool_ is True else client.DELETE,
            self.ctx(),
            '/relations',
            **{
                res1: self.pk(),
                res2: ",".join([str(obj.pk()) for obj in objs])
            }
        )
        # Dear Future Dev, if you're wondering why changes are disappearing
        # when relate/unrelate calls are made then this line is why, but
        # without it then relate/unrelate changes disappear on save calls.
        if refresh:
            for obj in objs:
                obj.refresh()
            self.refresh()

    def mock_set_relation_multiple(self, bool_, objs, refresh=True):
        self.mock_save()

    def to_dict(self):
        """ Retrieve a dictionary version of the model.
        """
        def collapse_dict(obj):
            dict_ = {}
            for key in dir(obj):
                value = getattr(obj, key)
                if value == None:
                    continue
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

    def mock_unrelate(self, obj):
        self.mock_set_relation(False, obj)

    def unrelate_many(self, objs):
        """ Unrelate this object and another object.
        """
        self.set_relation_multiple(False, objs)

    def mock_unnrelate_many(self, objs):
        self.mock_set_relation_multiple(False, objs)

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
        def cast_as_kind(value, kind, is_list):
            # Check for returning None
            if value is None:
                return None

            if isinstance(value, str) and isinstance(self.kind, str) and \
                    not value:
                return None

            if type(value).__name__ == 'unicode':
                # TODO: address this later
                value = value.encode('utf-8')

            if is_list:
                if not isinstance(value, list):
                    raise TypeError('Value: \'%s\' is not a list' % value)
                list_ = []
                for val in value:
                    list_.append(cast_as_kind(val, kind, False))
                return list_

            if isinstance(value, kind):
                value = value
            elif isinstance(value, int) and kind == float:
                value = float(value)
            elif isinstance(value, float) and kind == int:
                value = int(value)
            elif kind == int and isinstance(value, str):
                if value.isdigit():
                    value = int(value)
                elif value == '':
                    return None
                else:
                    raise TypeError(
                        'Type: \'%s\' for \'%s\' is not \'%s\'' % (
                            type(value), value, kind
                        )
                    )
            elif kind == bool and not isinstance(value, bool):
                raise TypeError(
                    'Type: \'%s\5 for \'%s\' is not \'%s\'' % (
                        type(value), value, kind
                    )
                )
            else:
                try:
                    value = kind(value)
                except:
                    raise TypeError(
                        'Type: \'%s\' for \'%s\' is not \'%s\'' % (
                            type(value), value, kind
                        )
                    )
            return value

        self.value = cast_as_kind(value, self.kind, self.is_list)


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


def resource(endpoint, pk='id'):
    """ This is a decorator for specifying a endpoint and what attribute
    stores the primary key for a model.
    """
    def set_resource(obj):
        obj._resource = endpoint
        return obj
    return set_resource
