from amber_lib import client, errors, query
from amber_lib.models import components
from amber_lib.models.bases import Model, Property, resource




class AssemblageElement(Model):
    class_name = Property(str)
    description = Property(str)
    id = Property(int)
    name = Property(str)
    table_name = Property(str)
    parent_name = Property(str)


AssemblageElement.child_component = Property(AssemblageElement)


@resource('assemblage')
class Assemblage(Model):
    assemblage_element_list = Property(AssemblageElement, True)
    id = Property(int)
    name = Property(str)
    description = Property(str)




@resource('products')
class Product(Model):
    apron = Property(components.Apron)
    arm = Property(components.Arm)
    assemblage_id = Property(int)
    audit = Property(components.Audit)
    base = Property(components.Base)
    base_guid = Property(str)
    brand = Property(components.Brand)
    bulb = Property(components.Bulb)
    category = Property(components.Category)
    collection = Property(components.Collection)
    com_col = Property(components.COMCOL)
    construction_information = Property(components.ConstructionInformation)
    cushions = Property(components.Cushions)
    description = Property(components.Description)
    doors = Property(components.Doors)
    drawers = Property(components.Drawers)
    durability = Property(components.Durability)
    electrical = Property(components.Electrical)
    fiber = Property(components.Fiber)
    flame = Property(components.Flame)
    footboard = Property(components.Footboard)
    footrest = Property(components.Footrest)
    frame = Property(components.Frame)
    glass = Property(components.Glass)
    groups = Property(components.Groups)
    guid = Property(str)
    headboard = Property(components.Headboard)
    id = Property(int)
    identity = Property(components.Identity)
    images = Property(components.Images)
    instruction = Property(components.Instruction)
    interior_dimension = Property(components.InteriorDimension)
    inventory = Property(components.Inventory)
    keyword = Property(components.Keyword)
    leather = Property(components.Leather)
    live_version = Property(int)
    manufacturer = Property(components.Manufacturer)
    option_sets = Property(components.OptionSets)
    ordering_information = Property(components.OrderingInformation)
    overall_dimension = Property(components.OverallDimension)
    owner_id = Property(int)
    owner_type = Property(str)
    pattern = Property(components.Pattern)
    pedestal = Property(components.Pedestal)
    pillows = Property(components.Pillows)
    pricing = Property(components.Pricing)
    product_type = Property(str)
    rug_construction = Property(components.RugConstruction)
    rug_pattern = Property(components.RugPattern)
    seat = Property(components.Seat)
    shade = Property(components.Shade)
    shelves = Property(components.Shelves)
    shipping_information = Property(components.ShippingInformation)
    side_rail = Property(components.SideRail)
    suspension_point = Property(components.SuspensionPoint)
    table_leaves = Property(components.TableLeaves)
    textile = Property(components.Textile)
    version_id = Property(int)
    visibility = Property(components.Visibility)
    weight = Property(components.Weight)

    def get_components(self):
        return {
            key: val for key, val in self.__dict__.items()
            if key != 'id' and not key.startswith('_')
        }

    def form_schema(self):
        """ Retrieve the Schema for the """
        if not self.category or not self.category.primary:
            return Model.form_schema(self)
        else:
            uri_params = {}
            if self.category.primary:
                uri_params['primary'] = self.category.primary
            if self.category.secondary:
                uri_params['secondary'] = self.category.secondary
            if self.category.tertiary:
                uri_params['tertiary'] = self.category.tertiary

            res_type = self._resource
            endpoint = '/form_schemas/%s' % res_type
            return client.send(
                client.GET,
                self.ctx(),
                endpoint,
                {},
                **uri_params
            )

    def search(self, filtering=None, batch_size=500, offset=0,  **kwargs):
        if filtering and isinstance(filtering, query.Predicate):
            filtering = query.WhereItem(pred=filtering)
        try:
            payload = client.send(
                client.GET,
                self._ctx,
                '/products_search',
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

    def set_relation(self, bool_, obj, refresh=True):
        """ Create or remove a relation between the current model and a
        different model.
        """
        self.save()
        res1 = self._resource
        res2 = obj._resource

        if res2 == res1:
            res1 = "groups"
            res2 = "products"

        payload = client.send(
            client.POST if bool_ is True else client.DELETE,
            self.ctx(),
            '/relations',
            **{
                res1: self.pk(),
                res2: obj.pk()
            }
        )
        # Dear Future Dev, if you're wondering why changes are disappearing
        # when relate/unrelate calls are made then this line is why, but
        # without it then relate/unrelate changes disappear on save calls.
        if refresh:
            obj.refresh()
            self.refresh()


    def set_relation_multiple(self, bool_, objs, refresh=True):
        """ Create or remove a relation between the current model and a
        different model.
        """
        self.save()
        res1 = self._resource
        if len(objs) == 0:
            raise Exception("Must provide at least one object to relate to.")
        if not isinstance(objs, list):
            raise Exception("Must provide a list of objects to relate to.")

        res2 = objs[0]._resource

        if res2 == res1:
            res1 = "groups"
            res2 = "products"

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





@resource('products')
class Group(Model):
    assemblage = Property(Assemblage)
    assemblage_id = Property(int)
    audit = Property(components.Audit)
    category = Property(components.Category)
    collection = Property(components.Collection)
    construction_information = Property(components.ConstructionInformation)
    description = Property(components.Description)
    groups = Property(components.Groups)
    id = Property(int)
    identity = Property(components.Identity)
    images = Property(components.Images)
    instruction = Property(components.Instruction)
    keyword = Property(components.Keyword)
    manufacturer = Property(components.Manufacturer)
    option_sets = Property(components.OptionSets)
    ordering_information = Property(components.OrderingInformation)
    overall_dimension = Property(components.OverallDimension)
    pricing = Property(components.Pricing)
    product_type = Property(str)
    inventory = Property(components.Inventory)
    shipping_information = Property(components.ShippingInformation)
    visibility = Property(components.Visibility)
    weight = Property(components.Weight)

    def get_components(self):
        return {
            key: val for key, val in self.__dict__.items()
            if key != 'id' and not key.startswith('_')
        }

    def form_schema(self):
        """ Retrieve the Schema for the """
        if not self.category or not self.category.primary:
            return Model.form_schema(self)
        else:
            uri_params = {}
            if self.category.primary:
                uri_params['primary'] = self.category.primary
            if self.category.secondary:
                uri_params['secondary'] = self.category.secondary
            if self.category.tertiary:
                uri_params['tertiary'] = self.category.tertiary

            endpoint = '/form_schemas/%s' % self._resource
            return client.send(
                client.GET,
                self.ctx(),
                endpoint,
                {},
                **uri_params
            )


@resource('products')
class Kit(Model):
    assemblage = Property(Assemblage)
    audit = Property(components.Audit)
    category = Property(components.Category)
    collection = Property(components.Collection)
    construction_information = Property(components.ConstructionInformation)
    description = Property(components.Description)
    groups = Property(components.Groups)
    id = Property(int)
    identity = Property(components.Identity)
    images = Property(components.Images)
    instruction = Property(components.Instruction)
    keyword = Property(components.Keyword)
    manufacturer = Property(components.Manufacturer)
    option_sets = Property(components.OptionSets)
    ordering_information = Property(components.OrderingInformation)
    overall_dimension = Property(components.OverallDimension)
    pricing = Property(components.Pricing)
    product_type = Property(str)
    inventory = Property(components.Inventory)
    shipping_information = Property(components.ShippingInformation)
    visibility = Property(components.Visibility)
    weight = Property(components.Weight)

    def get_components(self):
        return {
            key: val for key, val in self.__dict__.items()
            if key != 'id' and not key.startswith('_')
        }

    def form_schema(self):
        """ Retrieve the Schema for the """
        if not self.category or not self.category.primary:
            return Model.form_schema(self)
        else:
            uri_params = {}
            if self.category.primary:
                uri_params['primary'] = self.category.primary
            if self.category.secondary:
                uri_params['secondary'] = self.category.secondary
            if self.category.tertiary:
                uri_params['tertiary'] = self.category.tertiary

            endpoint = '/form_schemas/%s' % self._resource
            return client.send(
                client.GET,
                self.ctx(),
                endpoint,
                {},
                **uri_params
            )


@resource('kit_pieces')
class KitPiece(Model):
    assemblage = Property(Assemblage)
    audit = Property(components.Audit)
    brand = Property(components.Brand)
    collection = Property(components.Collection)
    description = Property(components.Description)
    id = Property(int)
    identity = Property(components.Identity)
    images = Property(components.Images)
    manufacturer = Property(components.Manufacturer)
    brand = Property(components.Brand)
    overall_dimension = Property(components.OverallDimension)
    pricing = Property(components.Pricing)
    product_type = Property(str)

    def get_components(self):
        return {
            key: val for key, val in self.__dict__.items()
            if key != 'id' and not key.startswith('_')
        }

    def form_schema(self):
        endpoint = '/form_schemas/%s' % self._resource
        return client.send(
            client.GET,
            self.ctx(),
            endpoint,
            {}
        )

    def search(self, filtering=None, batch_size=500, offset=0, **kwargs):
        if filtering and isinstance(filtering, query.Predicate):
            filtering = query.WhereItem(pred=filtering)
        payload = client.send(
            client.GET,
            self._ctx,
            '/kit_pieces_search',
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

        return collection


