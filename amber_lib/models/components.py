from amber_lib.models.bases import Component, resource
from amber_lib.models import primaries
from amber_lib.models.bases import Property


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
    height = Property(float)
    diameter = Property(float)
    depth = Property(float)
    width = Property(float)


@resource('box')
class Box(Component):
    weight = Property(float)
    width = Property(float)
    height = Property(float)
    depth = Property(float)


@resource('bulb')
class Bulb(Component):
    type = Property(str)
    base = Property(str)
    quantity = Property(int)
    wattage = Property(int)


@resource('category')
class Category(Component):
    primary = Property(str)
    secondary = Property(str)
    tertiary = Property(str)


@resource('collection')
class Collection(Component):
    collection_id = Property(int)
    collection = Property(primaries.Collection)


@resource('construction_information')
class ConstructionInformation(Component):
    material = Property(str)
    joinery_type = Property(str)


@resource('cushion')
class Cushion(Component):
    fill = Property(str)
    style = Property(str)
    width = Property(float)
    depth = Property(float)
    height = Property(float)


@resource('cushions')
class Cushions(Component):
    quantity = Property(int)
    cushion_list = Property(Cushion, True)


@resource('description')
class Description(Component):
    primary = Property(str)
    retail = Property(str)
    designer = Property(str)
    alternate = Property(str)
    features = Property(str)


@resource('door')
class Door(Component):
    width = Property(float)
    depth = Property(float)
    height = Property(float)
    opening = Property(float)


@resource('doors')
class Doors(Component):
    quantity = Property(int)
    door_list = Property(Door, True)


@resource('durability')
class Durability(Component):
    martindale = Property(str)
    wyzenbeek = Property(str)
    flammability = Property(str)


@resource('drawer')
class Drawer(Component):
    width = Property(float)
    depth = Property(float)
    height = Property(float)


@resource('drawers')
class Drawers(Component):
    quantity = Property(int)
    drawer_list = Property(Drawer, True)


@resource('electrical')
class Electrical(Component):
    switch_type = Property(str)
    voltage = Property(int)
    exterior_use = Property(bool)


@resource('fiber')
class Fiber(Component):
    pile = Property(str)
    construction = Property(str)


@resource('flame')
class Flame(Component):
    fuel_type = Property(str)
    burner_capacity = Property(float)
    burning_time = Property(float)
    heat_output = Property(float)
    minimum_room_size = Property(float)


@resource('footboard')
class Footboard(Component):
    height = Property(float)
    width = Property(float)
    depth = Property(float)
    floor_clearance = Property(float)


@resource('footrest')
class Footrest(Component):
    height = Property(float)


@resource('frame')
class Frame(Component):
    height = Property(float)
    back_rail_height = Property(float)


@resource('glass')
class Glass(Component):
    type = Property(str)


@resource('headboard')
class Headboard(Component):
    height = Property(float)
    width = Property(float)
    depth = Property(float)
    floor_clearance = Property(float)


@resource('identity')
class Identity(Component):
    name = Property(str)
    manufacturer_sku = Property(str)
    source_url = Property(str)
    alternate_name = Property(str)


@resource('instruction')
class Instruction(Component):
    cleaning_directions = Property(str)
    installation_directions = Property(str)


@resource('interior_dimension')
class InteriorDimension(Component):
    depth = Property(float)
    height = Property(float)
    width = Property(float)


@resource('image')
class Image(Component):
    default = Property(bool)
    category = Property(str)
    caption = Property(str)
    full_size = Property(str)
    large_size = Property(str)
    medium_size = Property(str)
    thumbnail_size = Property(str)


@resource('images')
class Images(Component):
    image_list = Property(Image, True)


@resource('leather')
class Leather(Component):
    type = Property(str)
    pattern_number = Property(str)
    hide_size = Property(float)
    finish = Property(str)
    col_requirement = Property(str)


@resource('manufacturer')
class Manufacturer(Component):
    manufacturer_id = Property(int)
    manufacturer = Property(primaries.Manufacturer)


@resource('pattern')
class Pattern(Component):
    pattern_number = Property(str)
    vertical_repeat = Property(float)
    horizontal_repeat = Property(float)
    direction = Property(str)
    color = Property(str)
    scale = Property(str)
    design_type = Property(str)


@resource('pedestal')
class Pedestal(Component):
    height = Property(float)
    diameter = Property(float)
    depth = Property(float)
    width = Property(float)


@resource('pricing')
class Pricing(Component):
    wholesale = Property(int)
    trade_price = Property(int)
    minimum_internet_price = Property(int)
    msrp = Property(int)
    dealer_price = Property(int)


@resource('promotional_tag')
class PromotionalTag(Component):
    new_product = Property(bool)
    best_seller = Property(bool)
    limited_stock = Property(bool)
    discontinued = Property(bool)


@resource('option_set')
class OptionSet(Component):
    option_set_id = Property(int)


@resource('option_sets')
class OptionSets(Component):
    option_set_list = Property(OptionSet, True)


@resource('ordering_information')
class OrderingInformation(Component):
    unit = Property(str)
    discontinued = Property(bool)
    lead_time = Property(str)
    quick_ship = Property(bool)
    minimum_quantity = Property(int)
    stock = Property(float)


@resource('overall_dimension')
class OverallDimension(Component):
    width = Property(float)
    height = Property(float)
    depth = Property(float)
    diameter = Property(float)


@resource('pillow')
class Pillow(Component):
    width = Property(float)
    height = Property(float)
    depth = Property(float)


@resource('pillows')
class Pillows(Component):
    quantity = Property(int)
    pillow_list = Property(Pillow, True)


@resource('seat')
class Seat(Component):
    height = Property(float)
    depth = Property(float)
    width = Property(float)
    construction = Property(str)


@resource('shade')
class Shade(Component):
    type = Property(str)
    height = Property(float)
    width = Property(float)
    depth = Property(float)
    diameter = Property(float)
    material = Property(str)
    quantity = Property(int)


@resource('shelf')
class Shelf(Component):
    width = Property(float)
    height = Property(float)
    depth = Property(float)


@resource('shelves')
class Shelves(Component):
    quantity = Property(int)
    shelf_list = Property(Shelf, True)


@resource('shipping_information')
class ShippingInformation(Component):
    ships_from = Property(str)
    volume = Property(float)
    standard = Property(bool)
    freight = Property(bool)
    white_glove = Property(bool)
    drop_ship = Property(bool)
    notes = Property(bool)
    box_list = Property(Box, True)


@resource('side_rail')
class SideRail(Component):
    length = Property(float)
    floor_clearance = Property(float)


@resource('suspension_point')
class SuspensionPoint(Component):
    support_type = Property(str)
    canopy_diameter = Property(float)
    canopy_depth = Property(float)
    canopy_height = Property(float)
    canopy_width = Property(float)
    wire_length = Property(float)
    minimum_hanging_length = Property(float)
    maximum_hanging_length = Property(float)
    chain_length = Property(float)


@resource('table_leaf')
class TableLeaf(Component):
    width = Property(float)
    depth = Property(float)


@resource('table_leaves')
class TableLeaves(Component):
    quantity = Property(int)
    table_leaf_list = Property(TableLeaf, True)


@resource('textile')
class Textile(Component):
    content = Property(str)
    weave_type = Property(str)
    width = Property(float)
    treatment = Property(str)
    usage = Property(str)
    grade = Property(str)
    com_requirement = Property(float)


@resource('weight')
class Weight(Component):
    weight = Property(float)


@resource('visibility')
class Visibility(Component):
    active = Property(bool)
    meets_posting_requirements = Property(bool)
