from amber_lib import client
from amber_lib.models import primaries
from amber_lib.models.bases import Model, Property, resource


class Component(Model):
    """ A layer on top of Model for handling differences between models and
    Component models.
    """

    _pk = "component_data_id"
    _resource = 'component'
    component_data_id = Property(int)
    parent_id = Property(int)
    parent_name = Property(str)
    product_id = Property(int)

    def delete(self, id_=None):
        """ Delete a component.
        """
        if id_ is not None:
            if self.is_valid() and self.pk() != id_:
                raise ValueError
            else:
                setattr(self, self._pk, id_)

        if self.is_valid():
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
        """ Retrieve the endpoint URL for the current component.
        """
        loc = "/components/%s" % self._resource

        if not self.is_valid():
            return loc

        if isinstance(self.pk(), int) and self.pk() > 0:
            return loc + "/%d" % self.pk()

    def retrieve(self, id_):
        """ Retreive a component by ID.
        """
        setattr(self, self._pk, id_)
        payload = client.send(
            client.GET,
            self.ctx(),
            self.endpoint(),
            None,
        )
        self.from_dict(payload)
        return self

    def save(self, data=None):
        """ Save the current data in the model to the API.
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

    def form_schema(self):
        """ Retrieve the Schema for the """
        endpoint = "/form_schemas/products?component=%s" % self._resource
        response = client.send(client.GET, self.ctx(), endpoint, {})
        return response


@resource('audit')
class Audit(Component):
    date_added = Property(str)
    date_updated = Property(str)
    updated_by_api_key = Property(str)


@resource('arm')
class Arm(Component):
    height = Property(float)
    style = Property(str)


@resource('base')
class Base(Component):
    depth = Property(float)
    diameter = Property(float)
    height = Property(float)
    width = Property(float)


@resource('box')
class Box(Component):
    depth = Property(float)
    height = Property(float)
    weight = Property(float)
    width = Property(float)
    quantity = Property(int)
    volume = Property(float)


@resource('bulb')
class Bulb(Component):
    base = Property(str)
    quantity = Property(int)
    type = Property(str)
    wattage = Property(int)


@resource('category')
class Category(Component):
    primary = Property(str)
    secondary = Property(str)
    tertiary = Property(str)


@resource('collection')
class Collection(Component):
    collection = Property(primaries.Collection)
    collection_id = Property(int)


@resource('construction_information')
class ConstructionInformation(Component):
    material = Property(str)
    joinery_type = Property(str)
    finish = Property(str)
    assembly_required = Property(bool)


@resource('cushion')
class Cushion(Component):
    depth = Property(float)
    fill = Property(str)
    height = Property(float)
    style = Property(str)
    width = Property(float)
    quantity = Property(int)


@resource('cushions')
class Cushions(Component):
    cushion_list = Property(Cushion, True)
    quantity = Property(int)


@resource('feature')
class Feature(Component):
    description = Property(str)


@resource('description')
class Description(Component):
    alternate = Property(str)
    designer = Property(str)
    feature_list = Property(Feature, True)
    primary = Property(str)
    retail = Property(str)


@resource('door')
class Door(Component):
    depth = Property(float)
    height = Property(float)
    opening = Property(float)
    width = Property(float)
    quantity = Property(int)


@resource('doors')
class Doors(Component):
    door_list = Property(Door, True)
    quantity = Property(int)


@resource('durability')
class Durability(Component):
    flammability = Property(str)
    martindale = Property(str)
    wyzenbeek = Property(str)


@resource('drawer')
class Drawer(Component):
    depth = Property(float)
    height = Property(float)
    width = Property(float)
    quantity = Property(int)


@resource('drawers')
class Drawers(Component):
    drawer_list = Property(Drawer, True)
    quantity = Property(int)


@resource('electrical')
class Electrical(Component):
    exterior_use = Property(bool)
    switch_type = Property(str)
    voltage = Property(int)


@resource('fiber')
class Fiber(Component):
    construction = Property(str)
    pile = Property(str)


@resource('flame')
class Flame(Component):
    burner_capacity = Property(float)
    burning_time = Property(float)
    fuel_type = Property(str)
    heat_output = Property(float)
    minimum_room_size = Property(float)


@resource('footboard')
class Footboard(Component):
    depth = Property(float)
    floor_clearance = Property(float)
    height = Property(float)
    width = Property(float)


@resource('footrest')
class Footrest(Component):
    height = Property(float)


@resource('frame')
class Frame(Component):
    back_rail_height = Property(float)
    height = Property(float)


@resource('glass')
class Glass(Component):
    type = Property(str)


@resource('headboard')
class Headboard(Component):
    depth = Property(float)
    floor_clearance = Property(float)
    height = Property(float)
    width = Property(float)


@resource('identity')
class Identity(Component):
    alternate_name = Property(str)
    manufacturer_sku = Property(str)
    name = Property(str)
    source_url = Property(str)


@resource('image')
class Image(Component):
    caption = Property(str)
    category = Property(str)
    default = Property(bool)
    full_size = Property(str)
    large_size = Property(str)
    medium_size = Property(str)
    thumbnail_size = Property(str)


@resource('images')
class Images(Component):
    image_list = Property(Image, True)


@resource('instruction')
class Instruction(Component):
    cleaning_directions = Property(str)
    installation_directions = Property(str)


@resource('interior_dimension')
class InteriorDimension(Component):
    depth = Property(float)
    height = Property(float)
    width = Property(float)


@resource('leather')
class Leather(Component):
    finish = Property(str)
    col_requirement = Property(str)
    hide_size = Property(float)
    pattern_number = Property(str)
    type = Property(str)


@resource('manufacturer')
class Manufacturer(Component):
    manufacturer = Property(primaries.Manufacturer)
    manufacturer_id = Property(int)


@resource('option_set')
class OptionSet(Component):
    option_set_id = Property(int)
    option_set = Property(primaries.OptionSet)

@resource('option_sets')
class OptionSets(Component):
    option_set_list = Property(OptionSet, True)


@resource('ordering_information')
class OrderingInformation(Component):
    discontinued = Property(bool)
    force_multiples = Property(int)
    lead_time = Property(str)
    minimum_quantity = Property(int)
    quick_ship = Property(bool)
    unit = Property(str)
    stock = Property(float)
    warranty = Property(str)

@resource('overall_dimension')
class OverallDimension(Component):
    depth = Property(float)
    diameter = Property(float)
    height = Property(float)
    width = Property(float)


@resource('pattern')
class Pattern(Component):
    color = Property(primaries.MultiValueList)
    design_type = Property(primaries.MultiValueList)
    direction = Property(str)
    horizontal_repeat = Property(float)
    pattern_number = Property(str)
    scale = Property(str)
    vertical_repeat = Property(float)


@resource('pedestal')
class Pedestal(Component):
    diameter = Property(float)
    depth = Property(float)
    height = Property(float)
    width = Property(float)


@resource('pillow')
class Pillow(Component):
    depth = Property(float)
    width = Property(float)
    height = Property(float)
    quantity = Property(int)


@resource('pillows')
class Pillows(Component):
    pillow_list = Property(Pillow, True)
    quantity = Property(int)


@resource('pricing')
class Pricing(Component):
    dealer_price = Property(int)
    minimum_internet_price = Property(int)
    msrp = Property(int)
    trade_price = Property(int)
    wholesale = Property(int)


@resource('promotional_tag')
class PromotionalTag(Component):
    best_seller = Property(bool)
    discontinued = Property(bool)
    limited_stock = Property(bool)
    new_product = Property(bool)


@resource('seat')
class Seat(Component):
    construction = Property(str)
    depth = Property(float)
    height = Property(float)
    width = Property(float)


@resource('shade')
class Shade(Component):
    depth = Property(float)
    diameter = Property(float)
    height = Property(float)
    material = Property(str)
    quantity = Property(int)
    type = Property(str)
    width = Property(float)


@resource('shelf')
class Shelf(Component):
    depth = Property(float)
    width = Property(float)
    height = Property(float)
    quantity = Property(int)


@resource('shelves')
class Shelves(Component):
    quantity = Property(int)
    shelf_list = Property(Shelf, True)


@resource('shipping_information')
class ShippingInformation(Component):
    box_list = Property(Box, True)
    drop_ship = Property(bool)
    freight = Property(bool)
    notes = Property(str)
    ships_from = Property(str)
    standard = Property(bool)
    volume = Property(float)
    white_glove = Property(bool)
    country_of_origin = Property(str)


@resource('side_rail')
class SideRail(Component):
    floor_clearance = Property(float)
    length = Property(float)


@resource('suspension_point')
class SuspensionPoint(Component):
    canopy_depth = Property(float)
    canopy_diameter = Property(float)
    canopy_height = Property(float)
    canopy_width = Property(float)
    chain_length = Property(float)
    maximum_hanging_length = Property(float)
    minimum_hanging_length = Property(float)
    support_type = Property(str)
    wire_length = Property(float)


@resource('table_leaf')
class TableLeaf(Component):
    depth = Property(float)
    width = Property(float)
    quantity = Property(int)


@resource('table_leaves')
class TableLeaves(Component):
    quantity = Property(int)
    table_leaf_list = Property(TableLeaf, True)


@resource('textile')
class Textile(Component):
    com_requirement = Property(float)
    content = Property(str)
    grade = Property(str)
    treatment = Property(str)
    usage = Property(primaries.MultiValueList)
    weave_type = Property(primaries.MultiValueList)
    width = Property(float)


@resource('weight')
class Weight(Component):
    weight = Property(float)


@resource('visibility')
class Visibility(Component):
    active = Property(bool)
    meets_posting_requirements = Property(bool)
