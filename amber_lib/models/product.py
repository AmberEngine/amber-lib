from amber_lib import client
from amber_lib.models import components
from amber_lib.models.bases import Model, Property, resource
from amber_lib.models.primaries import Assemblage


@resource('products')
class Product(Model):
    id = Property(int)
    assemblage = Property(Assemblage)
    apron = Property(components.Apron)
    arm = Property(components.Arm)
    audit = Property(components.Audit)
    base = Property(components.Base)
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
    headboard = Property(components.Headboard)
    identity = Property(components.Identity)
    images = Property(components.Images)
    interior_dimension = Property(components.InteriorDimension)
    instruction = Property(components.Instruction)
    keyword = Property(components.Keyword)
    leather = Property(components.Leather)
    manufacturer = Property(components.Manufacturer)
    option_sets = Property(components.OptionSets)
    ordering_information = Property(components.OrderingInformation)
    pattern = Property(components.Pattern)
    pricing = Property(components.Pricing)
    pedestal = Property(components.Pedestal)
    pillows = Property(components.Pillows)
    promotional_tag = Property(components.PromotionalTag)
    overall_dimension = Property(components.OverallDimension)
    rug_construction = Property(components.RugConstruction)
    rug_pattern = Property(components.RugPattern)
    seat = Property(components.Seat)
    shade = Property(components.Shade)
    side_rail = Property(components.SideRail)
    shelves = Property(components.Shelves)
    shipping_information = Property(components.ShippingInformation)
    suspension_point = Property(components.SuspensionPoint)
    table_leaves = Property(components.TableLeaves)
    textile = Property(components.Textile)
    visibility = Property(components.Visibility)
    weight = Property(components.Weight)

    def get_components(self):
        return {
            key: val for key, val in self.__dict__.items()
            if key != 'id' and not key.startswith('_')
        }

    def form_schema(self):
        """ Retrieve the Schema for the """
        if not self.category.primary:
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

    def search(self, filtering=None, batch_size=500, offset=0,  **kwargs):
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

        return collection
