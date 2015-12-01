import amberlib.models.base as base


class Audit(base.Component):
    date_added = Property(str)
    date_updated = Property(str)
    updated_by_api_key = Property(str)


class Arm(base.Component):
    height = Property(float)
    style = Property(str)


class Assemblage(base.Component):
    id = Property(int)
    name = Property(str)
    description = Property(str)
    table_name = Property(str)
    class_name = Property(str)
    parent_name = Property(str)
    child_component = Property(Assemblage)


class Base(base.Component):
    height = Property(float)
    diameter = Property(float)
    depth = Property(float)
    width = Property(float)


class Box(bases.Component):
    weight = Property(float)
    width = Property(float)
    height = Property(float)
    depth = Property(float)


class Bulb(base.Component):
    type = Property(str)
    base = Property(str)
    quantity = Property(int)
    wattage = Property(int)


class Category(base.Component):
    primary = Property(str)
    secondary = Property(str)
    tertiary = Property(str)


class Collection(base.Component):
    collection_id = Property(int)
    collection = Property(models.primaries.Collection)


class ConstructionInformation(base.Component):
    material = Property(str)
    joinery_type = Property(str)


class Cushion(bases.Component):
    fill = Property(str)
    style = Property(str)
    width = Property(float)
    depth = Property(float)
    height = Property(float)


class Cushions(base.Component):
    quantity = Property(int)
    cushion_list = Property(Cushion, true)


class Description(base.Component):
    primary = Property(str)
    retail = Property(str)
    designer = Property(str)
    alterate = Property(str)
    features = Property(str)


class Door(base.Component):
    width = Property(float)
    depth = Property(float)
    height = Property(float)
    opening = Property(float)


class Doors(base.Component):
    quanitity = Property(int)
    door_list = Property(Door, true)


class Durability(base.Component):
    martindale = Property(str)
    wyzenbeek = Property(str)
    flammability = Property(str)


class Drawer(base.Component):
    width = Property(float)
    depth = Property(float)
    height = Property(float)


class Drawers(base.Component):
    quantity = Property(int)
    drawer_list = Property(Drawer, true)


class Electrical(base.Component):
    switch_type = Property(str)
    voltage = Property(int)
    exterior_use = Property(bool)


class Fiber(base.Component):
    pile = Property(str)
    construction = Property(str)


class Flame(base.Component):
    fuel_type = Property(str)
    burner_capacity = Property(float)
    burning_time = Property(float)
    heat_output = Property(float)
    minimum_room_size = Property(float)


class Footboard(base.Component):
    height = Property(float)
    width = Property(float)
    depth = Property(float)
    floor_clearance = Property(float)


class Footrest(base.Component):
    height = Property(float)


class Frame(base.Component):
    height = Property(float)
    back_rail_height = Property(float)


class Glass(base.Component):
    type = Property(str)


class Headboard(base.Component):
    height = Property(float)
    width = Property(float)
    depth = Property(float)
    floor_clearance = Property(float)


class Identity(base.Component):
    name = Property(str)
    manufacturer_sku = Property(str)
    source_url = Property(str)
    alternate_name = Property(str)


class Instructions(base.Component):
    cleaning_directions = Property(str)
    installation_directions = Property(str)


class InteriorDimension(base.Component):
    depth = Property(float)
    height = Property(float)
    width = Property(float)


class Image(bases.Component):
    default = Property(bool)
    category = Property(str)
    caption = Property(str)
    fullsize = Property(str)
    large_size = Property(str)
    medium_size = Property(str)
    thumbnail_size = Property(str)


class Images(base.Component):
    image_list = Property(Image)


class Leather(base.Component):
    type = Property(str)
    pattern_number = Property(str)
    hide_size = Property(float)
    finish = Property(str)
    col_requirement = Property(str)


class Manufacturer(base.Component):
    manufacturer_id = Property(int)
    manufacturer = Property(models.primaries.Manufacturer)


class Pattern(base.Component):
    pattern_number = Property(str)
    vertical_repeat = Property(float)
    horizontal_repeat = Property(float)
    direction = Property(str)
    color = Property(str)
    scale = Property(str)
    design_type = Property(str)


class Pedestal(base.Component):
    height = Property(float)
    diameter = Property(float)
    depth = Property(float)
    width = Property(float)


class Pricing(base.Component):
    wholesale = Property(int)
    trade_price = Property(int)
    minimum_internet_price = Property(int)
    msrp = Property(int)
    dealer_price = Property(int)


class PromotionalTags(base.Component):
    new_product = Property(bool)
    best_seller = Property(bool)
    limited_stock = Property(bool)
    discontinued = Property(bool)


class OptionSets(base.Component):
    option_set_list = Property(models.primaries.OptionSet, true)


class OrderingInformation(base.Component):
    unit = Property(str)
    discontinued = Property(bool)
    lead_time = Property(str)
    quick_ship = Property(bool)
    minimum_quanitity = Property(int)
    stock = Property(float)


class OverallDimensions(base.Component):
    width = Property(float)
    height = Property(float)
    depth = Property(float)
    diameter = Property(float)


class Pillow(bases.Component):
    width = Property(float)
    height = Property(float)
    depth = Property(float)


class Pillows(base.Component):
    quantity = Property(int)
    pillow_list = Property(Pillow, true)


class Seat(base.Component):
    height = Property(float)
    depth = Property(float)
    width = Property(float)
    construction = Property(str)


class Shade(base.Component):
    type = Property(str)
    height = Property(float)
    width = Property(float)
    depth = Property(float)
    diameter = Property(float)
    material = Property(str)
    quantity = Property(int)


class Shelf(base.Component):
    width = Property(float)
    height = Property(float)
    depth = Property(float)


class Shelves(base.Component):
    quantity = Property(int)
    shelf_list = Property(Shelf, true)


class ShippingInformation(base.Component):
    ships_from = Property(str)
    volume = Property(float)
    standard = Property(bool)
    freight = Property(bool)
    white_glove = Property(bool)
    drop_ship = Property(bool)
    notes = Property(bool)
    box_list = Property(Box, true)


class SideRail(base.Component):
    length = Property(float)
    floor_clearance = Property(float)


class Suspension(base.Component):
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


class TableLeaves(base.Component):
    quantity = Property(int)
    table_leaf_list = Property(TableLeaf, true)


class Textile(base.Component):
    content = Property(str)
    weave_type = Property(str)
    width = Property(float)
    treatment = Property(str)
    usage = Property(str)
    grade = Property(str)
    com_requirement = Property(float)


class Weight(base.Component):
    weight = Property(float)


class Visibility(base.Component):
    active = Property(bool)
    meets_posting_requirements = Property(bool)
