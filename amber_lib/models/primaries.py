from amber_lib.models.bases import Model, resource
from amber_lib.models.bases import Property

@resource('api_key')
class APIKey(Model):
    id = Property(int)
    name = Property(str)
    public = Property(str)
    private = Property(str)
    type = Property(str)
    manufacturer_id = Property(int)
    sales_channel_id = Property(int)


class AssemblageElement(Model):
    table_name = Property(str)
    class_name = Property(str)
    parent_name = Property(str)
    name = Property(str)
    id = Property(int)
    description = Property(str)


AssemblageElement.child_component = Property(AssemblageElement)


@resource('assemblage')
class Assemblage(Model):
    id = Property(int)
    name = Property(str)
    description = Property(str)
    assemblage_element_list = Property(AssemblageElement, True)


@resource('collection')
class Collection(Model):
    id = Property(int)
    manufacturer_id = Property(int)
    description = Property(str)
    designed_by = Property(str)


@resource('event')
class Event(Model):
    id = Property(int)
    name = Property(str)
    message = Property(str)
    object_id = Property(int)
    object_type = Property(str)
    date_time = Property(str)


@resource('export')
class Export:
    pass


@resource('manufacturer')
class Manufacturer(Model):
    id = Property(int)
    name = Property(str)
    bio = Property(str)
    url = Property(str)
    logo_url = Property(str)
    date_added = Property(str)
    date_updated = Property(str)
    date_profile_complete = Property(str)
    updated_by_api_key = Property(str)
    active = Property(bool)
    street_address_1 = Property(str)
    street_address_2 = Property(str)
    city = Property(str)
    state = Property(str)
    zipcode = Property(str)
    email = Property(str)
    phone = Property(str)
    phone_extension = Property(str)
    linkedin_url = Property(str)
    facebook_url = Property(str)
    google_plus_url = Property(str)
    twitter_url = Property(str)
    pinterest_url = Property(str)
    legal = Property(str)
    featured = Property(bool)
    restock_fee = Property(int)
    returnable = Property(bool)
    return_period = Property(int)

@resource('manufacturer_image')
class ManufacturerImage(Model):
    id = Property(int)
    manufacturer_id = Property(int)
    default = Property(bool)
    caption = Property(str)
    url = Property(str)


@resource('option_sets')
class OptionSet(Model):
    id = Property(int)
    manufacturer_id = Property(int)
    name = Property(str)
    type = Property(str)


@resource('sales_channel')
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


@resource('sales_channel_preference')
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
