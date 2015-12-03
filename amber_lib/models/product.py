from amber_lib.models.bases import Model, Property
from amber_lib.models.primaries import Assemblage
from amber_lib.models import components


class Product(Model):
    id = Property(int)
    assemblage = Property(Assemblage)
    arm = Property(components.Arm)
    audit = Property(components.Audit)
    category = Property(components.Category)
    collection = Property(components.Collection)
    construction_information = Property(components.ConstructionInformation)
    cushion = Property(components.Cushion)
    description = Property(components.Description)
    doors = Property(components.Doors)
    drawers = Property(components.Drawers)
    durability = Property(components.Durability)
    footrest = Property(components.Footrest)
    identity = Property(components.Identity)
    images = Property(components.Images)
    instructions = Property(components.Instructions)
    manufacturer = Property(components.Manufacturer)
    option_sets = Property(components.OptionSets)
    ordering_information = Property(components.OrderingInformation)
    pattern = Property(components.Pattern)
    pricing = Property(components.Pricing)
    pedestal = Property(components.Pedestal)
    pillows = Property(components.Pillows)
    promotional_tags = Property(components.PromotionalTags)
    overall_dimensions = Property(components.OverallDimensions)
    seat = Property(components.Seat)
    shelves = Property(components.Shelves)
    shipping_information = Property(components.ShippingInformation)
    table_leaves = Property(components.TableLeaves)
    textile = Property(components.Textile)
    visibility = Property(components.Visibility)
    weight = Property(components.Weight)

