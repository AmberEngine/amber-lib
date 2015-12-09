from amber_lib.models import bases
from amber_lib.models import primaries
from amber_lib.models.bases import Property


class Audit(bases.Component):
    date_added = Property(str)
    date_updated = Property(str)
    updated_by_api_key = Property(str)


class Arm(bases.Component):
    height = Property(float)
    style = Property(str)


class Base(bases.Component):
    height = Property(float)
    diameter = Property(float)
    depth = Property(float)
    width = Property(float)


class Box(bases.Component):
    weight = Property(float)
    width = Property(float)
    height = Property(float)
    depth = Property(float)


class Bulb(bases.Component):
    type = Property(str)
    base = Property(str)
    quantity = Property(int)
    wattage = Property(int)


class Category(bases.Component):
    primary = Property(str)
    secondary = Property(str)
    tertiary = Property(str)


class Collection(bases.Component):
    collection_id = Property(int)
    collection = Property(primaries.Collection)


class ConstructionInformation(bases.Component):
    material = Property(str)
    joinery_type = Property(str)


class Cushion(bases.Component):
    fill = Property(str)
    style = Property(str)
    width = Property(float)
    depth = Property(float)
    height = Property(float)


class Cushions(bases.Component):
    quantity = Property(int)
    cushion_list = Property(Cushion, True)


class Description(bases.Component):
    primary = Property(str)
    retail = Property(str)
    designer = Property(str)
    alternate = Property(str)
    features = Property(str)


class Door(bases.Component):
    width = Property(float)
    depth = Property(float)
    height = Property(float)
    opening = Property(float)


class Doors(bases.Component):
    quantity = Property(int)
    door_list = Property(Door, True)


class Durability(bases.Component):
    martindale = Property(str)
    wyzenbeek = Property(str)
    flammability = Property(str)


class Drawer(bases.Component):
    width = Property(float)
    depth = Property(float)
    height = Property(float)


class Drawers(bases.Component):
    quantity = Property(int)
    drawer_list = Property(Drawer, True)


class Electrical(bases.Component):
    switch_type = Property(str)
    voltage = Property(int)
    exterior_use = Property(bool)


class Fiber(bases.Component):
    pile = Property(str)
    construction = Property(str)


class Flame(bases.Component):
    fuel_type = Property(str)
    burner_capacity = Property(float)
    burning_time = Property(float)
    heat_output = Property(float)
    minimum_room_size = Property(float)


class Footboard(bases.Component):
    height = Property(float)
    width = Property(float)
    depth = Property(float)
    floor_clearance = Property(float)


class Footrest(bases.Component):
    height = Property(float)


class Frame(bases.Component):
    height = Property(float)
    back_rail_height = Property(float)


class Glass(bases.Component):
    type = Property(str)


class Headboard(bases.Component):
    height = Property(float)
    width = Property(float)
    depth = Property(float)
    floor_clearance = Property(float)


class Identity(bases.Component):
    name = Property(str)
    manufacturer_sku = Property(str)
    source_url = Property(str)
    alternate_name = Property(str)


class Instructions(bases.Component):
    cleaning_directions = Property(str)
    installation_directions = Property(str)


class InteriorDimension(bases.Component):
    depth = Property(float)
    height = Property(float)
    width = Property(float)


class Image(bases.Component):
    default = Property(bool)
    category = Property(str)
    caption = Property(str)
    full_size = Property(str)
    large_size = Property(str)
    medium_size = Property(str)
    thumbnail_size = Property(str)


class Images(bases.Component):
    image_list = Property(Image, True)


class Leather(bases.Component):
    type = Property(str)
    pattern_number = Property(str)
    hide_size = Property(float)
    finish = Property(str)
    col_requirement = Property(str)


class Manufacturer(bases.Component):
    manufacturer_id = Property(int)
    manufacturer = Property(primaries.Manufacturer)


class Pattern(bases.Component):
    pattern_number = Property(str)
    vertical_repeat = Property(float)
    horizontal_repeat = Property(float)
    direction = Property(str)
    color = Property(str)
    scale = Property(str)
    design_type = Property(str)


class Pedestal(bases.Component):
    height = Property(float)
    diameter = Property(float)
    depth = Property(float)
    width = Property(float)


class Pricing(bases.Component):
    wholesale = Property(int)
    trade_price = Property(int)
    minimum_internet_price = Property(int)
    msrp = Property(int)
    dealer_price = Property(int)


class PromotionalTags(bases.Component):
    new_product = Property(bool)
    best_seller = Property(bool)
    limited_stock = Property(bool)
    discontinued = Property(bool)


class OptionSets(bases.Component):
    option_set_list = Property(primaries.OptionSet, True)


class OrderingInformation(bases.Component):
    unit = Property(str)
    discontinued = Property(bool)
    lead_time = Property(str)
    quick_ship = Property(bool)
    minimum_quantity = Property(int)
    stock = Property(float)


class OverallDimensions(bases.Component):
    width = Property(float)
    height = Property(float)
    depth = Property(float)
    diameter = Property(float)


class Pillow(bases.Component):
    width = Property(float)
    height = Property(float)
    depth = Property(float)


class Pillows(bases.Component):
    quantity = Property(int)
    pillow_list = Property(Pillow, True)


class Seat(bases.Component):
    height = Property(float)
    depth = Property(float)
    width = Property(float)
    construction = Property(str)


class Shade(bases.Component):
    type = Property(str)
    height = Property(float)
    width = Property(float)
    depth = Property(float)
    diameter = Property(float)
    material = Property(str)
    quantity = Property(int)


class Shelf(bases.Component):
    width = Property(float)
    height = Property(float)
    depth = Property(float)


class Shelves(bases.Component):
    quantity = Property(int)
    shelf_list = Property(Shelf, True)


class ShippingInformation(bases.Component):
    ships_from = Property(str)
    volume = Property(float)
    standard = Property(bool)
    freight = Property(bool)
    white_glove = Property(bool)
    drop_ship = Property(bool)
    notes = Property(bool)
    box_list = Property(Box, True)


class SideRail(bases.Component):
    length = Property(float)
    floor_clearance = Property(float)


class SuspensionPoint(bases.Component):
    support_type = Property(str)
    canopy_diameter = Property(float)
    canopy_depth = Property(float)
    canopy_height = Property(float)
    canopy_width = Property(float)
    wire_length = Property(float)
    minimum_hanging_length = Property(float)
    maximum_hanging_length = Property(float)
    chain_length = Property(float)


class TableLeaf(bases.Component):
    width = Property(float)
    depth = Property(float)


class TableLeaves(bases.Component):
    quantity = Property(int)
    table_leaf_list = Property(TableLeaf, True)


class Textile(bases.Component):
    content = Property(str)
    weave_type = Property(str)
    width = Property(float)
    treatment = Property(str)
    usage = Property(str)
    grade = Property(str)
    com_requirement = Property(float)


class Weight(bases.Component):
    weight = Property(float)


class Visibility(bases.Component):
    active = Property(bool)
    meets_posting_requirements = Property(bool)
