from amber_lib.models.bases import Model
from amber_lib.models.bases import Property


class APIKey(Model):
    id = Property(int)
    name = Property(str)
    public = Property(str)
    private = Property(str)
    type = Property(str)
    manufacturer_id = Property(int)
    sales_channel_id = Property(int)


class Collection(Model):
    id = Property(int)
    manufacturer_id = Property(int)
    description = Property(str)
    designed_by = Property(str)


class Event(Model):
    id = Property(int)
    name = Property(str)
    message = Property(str)
    object_id = Property(int)
    object_type = Property(str)
    date_time = Property(str)


class Export:
    pass


class Manufacturer:
    id = Property(int)
    name = Property(str)
    bio = Property(str)
    url = Property(str)
    logo_url = Property(str)
    date_added = Property(str)
    date_updated = Property(str)
    date_profile_complete = Property(str)
    update_by_api_key = Property(str)
    active = Property(bool)
    city = Property(str)
    email = Property(str)
    facebook_url = Property(str)
    google_plus_url = Property(str)
    legal = Property(str)


class ManufacturerImage(Model):
    id = Property(int)
    manufacturer_id = Property(int)
    default = Property(bool)
    caption = Property(str)
    url = Property(str)


class OptionSet(Model):
    id = Property(int)
    manufacturer_id = Property(int)
    name = Property(str)
    type = Property(str)


class Product(Model):
    from amber_lib.models import components
    id = Property(int)
    assemblage = Property(components.Assemblage)
    arm = Property(components.Arm)
    audit = Property(components.Audit)
    category = Property(components.Category)
    collection = Property(components.Collection)
    construction_information = Property(components.ConstructionInformation)
    cushion = Property(components.Cushion)
    description = Property(components.Description)
    door = Property(components.Door)
    drawer = Property(components.Drawer)
    durability = Property(components.Durability)
    footrest = Property(components.Footrest)
    identity = Property(components.Identity)
    image = Property(components.Image)
    instructions = Property(components.Instructions)
    manufacturer = Property(components.Manufacturer)
    option = Property(components.OptionSet)
    ordering_information = Property(components.OrderingInformation)
    pattern = Property(components.Pattern)
    pricing = Property(components.Pricing)
    pedestal = Property(components.Pedestal)
    pillow = Property(components.Pillow)
    promotional_tags = Property(components.PromotionalTags)
    overall_dimensions = Property(components.OverallDimensions)
    seat = Property(components.Seat)
    shelf = Property(components.Shelf)
    shipping_information = Property(components.ShippingInformation)
    table_leaf = Property(components.TableLeaf)
    textile = Property(components.Textile)
    visibility = Property(components.Visibility)
    weight = Property(components.Weight)


class SalesChannel(Model):
    id = Property(int)
    api_key_id = Property(int)
    visible = Property(bool)
    name = Property(str)
    bio = Property(str)
    url = Property(str)
    logo_url = Property(str)
    phone = Property(str)
    extension = Property(str)
    street_address_1 = Property(str)
    street_address_2 = Property(str)
    city = Property(str)
    state = Property(str)
    zipcode = Property(str)
    facebook_url = Property(str)
    google_plus_url = Property(str)
    linkedin_url = Property(str)
    pinterest_url = Property(str)
    twitter_url = Property(str)
    setting_image = Property(bool)
    isolated_image = Property(bool)
    other_image = Property(bool)


class SalesChannelPreference(Model):
    id = Property(int)
    manufacturer_id = Property(int)
    sales_channel_id = Property(int)
    active = Property(bool)
    description_description = Property(str)
    identity_name = Property(str)
    pricing_dealer_price = Property(bool)
    pricing_minimum_internet_price = Property(bool)
    pricing_msrp = Property(bool)
    pricing_trade_price = Property(bool)
    pricing_wholesale = Property(bool)
