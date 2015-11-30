import amberlib.models.base as base


class Audit(base.Component):
    attributes = {
        "date_added": Property(str),
        "date_updated": Property(str),
        "updated_by_api_key": Property(str)
    }


class Arm(base.Component):
    attributes = {
        "height": Property(float),
        "style": Property(str)
    }


class Assemblage(base.Component):
    attributes = {
        "id": Property(int),
        "name": Property(str),
        "description": Property(str),
        "table_name": Property(str),
        "class_name": Property(str),
        "parent_name": Property(str),
        "child_component": Property(models.components.Assemblage)
    }


class Base(base.Component):
    attributes = {
        "height": Property(float),
        "diameter": Property(float),
        "depth": Property(float),
        "width": Property(float)
    }


class Bulb(base.Component):
    attributes = {
        "type": Property(str),
        "base": Property(str),
        "quantity": Property(int),
        "wattage": Property(int)
    }


class Category(base.Component):
    attributes = {
        "primary": Property(str),
        "secondary": Property(str),
        "tertiary": Property(str)
    }


class Collection(base.Component):
    attributes = {
        "collection_id": Property(int),
        "collection": Property(models.primaries.Collection)
    }


class ConstructionInformation(base.Component):
    attributes = {
        "material": Property(str),
        "joinery_type": Property(str)
    }


class Cushion(base.Component):
    # TODO: Fix sub-component name.
    attributes = {
        "quantity": Property(int),
        "cushions": Property(models.components.Cushion, true)
    }


class Description(base.Component):
    attributes = {
        "primary": Property(str),
        "retail": Property(str),
        "designer": Property(str),
        "alterate": Property(str),
        "features": Property(str)
    }


class Door(base.Component):
    # TODO: Fix sub-component name!
    attributes = {
        "quanitity": Property(int),
        "doors": Property(models.components.Door, true)
    }


class Durability(base.Component):
    attributes = {
        "martindale": Property(str),
        "wyzenbeek": Property(str),
        "flammability": Property(str)
    }


class Drawer(base.Component):
    # TODO: Fix sub-component name.
    attributes = {
        "quantity": Property(int),
        "drawers": Property(model.components.Drawer, true)
    }


class Electrical(base.Component):
    attributes = {
        "switch_type": Property(str),
        "voltage": Property(int),
        "exterior_use": Property(bool)
    }


class Fiber(base.Component):
    attributes = {
        "pile": Property(str),
        "construction": Property(str)
    }


class Flame(base.Component):
    attributes = {
        "fuel_type": Property(str),
        "burner_capacity": Property(float),
        "burning_time": Property(float),
        "heat_output": Property(float),
        "minimum_room_size": Property(float)
    }


class Footboard(base.Component):
    attributes = {
        "height": Property(float),
        "width": Property(float),
        "depth": Property(float),
        "floor_clearance": Property(float)
    }


class Footrest(base.Component):
    attributes = {
        "height": Property(float)
    }


class Frame(base.Component):
    attributes = {
        "height": Property(float),
        "back_rail_height": Property(float)
    }


class Glass(base.Component):
    attributes = {
        "type": Property(str)
    }


class Headboard(base.Component):
    attributes = {
        "height": Property(float),
        "width": Property(float),
        "depth": Property(float),
        "floor_clearance": Property(float)
    }


class Identity(base.Component):
    attributes = {
        "name": Property(str),
        "manufacturer_sku": Property(str),
        "source_url": Property(str),
        "alternate_name": Property(str)
    }


class Instructions(base.Component):
    attributes = {
        "cleaning_directions": Property(str),
        "installation_directions": Property(str)
    }


class InteriorDimension(base.Component):
    attributes = {
        "depth": Property(float),
        "height": Property(float),
        "width": Property(float)
    }


class Image(base.Component):
    attributes = {
        "images": Property(models.components.Images)  # TODO: fix this!
    }


class Leather(base.Component):
    attributes = {
        "type": Property(str),
        "pattern_number": Property(str),
        "hide_size": Property(float),
        "finish": Property(str),
        "col_requirement": Property(str)
    }


class Manufacturer(base.Component):
    attributes = {
        "manufacturer_id": Property(int),
        "manufacturer": Property(models.primaries.Manufacturer)
    }


class Pattern(base.Component):
    attributes = {
        "pattern_number": Property(str),
        "vertical_repeat": Property(float),
        "horizontal_repeat": Property(float),
        "direction": Property(str),
        "color": Property(str),
        "scale": Property(str),
        "design_type": Property(str)
    }


class Pedestal(base.Component):
    attributes = {
        "height": Property(float),
        "diameter": Property(float),
        "depth": Property(float),
        "width": Property(float)
    }


class Pricing(base.Component):
    # TODO: These are INTs because we are working in cents, yes?
    attributes = {
        "wholesale": Property(int),
        "trade_price": Property(int),
        "minimum_internet_price": Property(int),
        "msrp": Property(int),
        "dealer_price": Property(int)
    }


class PromotionalTags(base.Component):
    attributes = {
        "new_product": Property(bool),
        "best_seller": Property(bool),
        "limited_stock": Property(bool),
        "discontinued": Property(bool)
    }


class Option(base.Component):
    # TODO: Is this even close to being right?
    attributes = {
        "option_sets": Property([models.components.Options])
    }


class OrderingInformation(base.Component):
    attributes = {
        "unit": Property(str),
        "discontinued": Property(bool),
        "lead_time": Property(str),
        "quick_ship": Property(bool),
        "minimum_quanitity": Property(int),
        "stock": Property(float)
    }


class OverallDimensions(base.Component):
    attributes = {
        "width": Property(float),
        "height": Property(float),
        "depth": Property(float),
        "diameter": Property(float)
    }


class Pillow(base.Component):
    # TODO: Fix sub-component name!
    attributes = {
        "quantity": Property(int),
        "pillows": Property(model.components.Pillows, true)
    }


class Seat(base.Component):
    attributes = {
        "height": Property(float),
        "depth": Property(float),
        "width": Property(float),
        "construction": Property(str)
    }


class Shade(base.Component):
    attributes = {
        "type": Property(str),
        "height": Property(float),
        "width": Property(float),
        "depth": Property(float),
        "diameter": Property(float),
        "material": Property(str),
        "quantity": Property(int)
    }


class Shelf(base.Component):
    # TODO: Fix sub-component name!
    attributes = {
        "quantity": Property(int),
        "shelves": Property(models.components.Shelf, true)
    }


class ShippingInformation(base.Component):
    attributes = {
        "ships_from": Property(str),
        "volume": Property(float),
        "standard": Property(bool),
        "freight": Property(bool),
        "white_glove": Property(bool),
        "drop_ship": Property(bool),
        "notes": Property(bool),
        "boxes": Property(models.components.Box, true)
    }


class SideRail(base.Component):
    attributes = {
        "length": Property(float),
        "floor_clearance": Property(float)
    }


class Suspension(base.Component):
    attributes = {
        "support_type": Property(str),
        "canopy_diameter": Property(float),
        "canopy_depth": Property(float),
        "canopy_height": Property(float),
        "canopy_width": Property(float),
        "wire_length": Property(float),
        "minimum_hanging_length": Property(float),
        "maximum_hanging_length": Property(float),
        "chain_length": Property(float)
    }


class TableLeaf(base.Component):
    # TODO: Fix sub-component name!
    attributes = {
        "quantity": Property(int),
        "table_leaves": Property(models.components.TableLeave, true)
    }


class Textile(base.Component):
    attributes = {
        "content": Property(str),
        "weave_type": Property(str),
        "width": Property(float),
        "treatment": Property(str),
        "usage": Property(str),
        "grade": Property(str),
        "com_requirement": Property(float)
    }


class Weight(base.Component):
    attributes = {
        "weight": Property(float)
    }


class Visibility(base.Component):
    attributes = {
        "active": Property(bool),
        "meets_posting_requirements": Property(bool)
    }
