from amber_lib.models.bases import Model, Property, resource


@resource('api_keys')
class APIKey(Model):
    id = Property(int)
    manufacturer_id = Property(int)
    name = Property(str)
    private = Property(str)
    public = Property(str)
    sales_channel_id = Property(int)
    type = Property(str)


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


@resource('categories')
class Categories(Model):
    primaries = Property(str, True)
    secondaries = Property(str, True)
    tertiaries = Property(str, True)

    class Count(Model):
        primary_categories = Property(int)
        secondary_categories = Property(int)
        tertiary_categories = Property(int)
    count = Property(Count)

    total = Property(int)

    def delete(self):
        pass

    def query(self):
        pass

@resource('collections')
class Collection(Model):
    description = Property(str)
    designed_by = Property(str)
    id = Property(int)
    manufacturer_id = Property(int)
    name = Property(str)


@resource('events')
class Event(Model):
    date_time = Property(str)
    id = Property(int)
    message = Property(str)
    name = Property(str)
    object_id = Property(int)
    object_type = Property(str)


@resource('exports')
class Export:
    pass


@resource('manufacturers')
class Manufacturer(Model):
    active = Property(bool)
    bio = Property(str)
    city = Property(str)
    date_added = Property(str)
    date_profile_complete = Property(str)
    date_updated = Property(str)
    email = Property(str)
    facebook_url = Property(str)
    featured = Property(bool)
    google_plus_url = Property(str)
    id = Property(int)
    legal = Property(str)
    linkedin_url = Property(str)
    logo_url = Property(str)
    name = Property(str)
    phone = Property(str)
    phone_extension = Property(str)
    pinterest_url = Property(str)
    restock_fee = Property(int)
    return_period = Property(int)
    returnable = Property(bool)
    state = Property(str)
    street_address_1 = Property(str)
    street_address_2 = Property(str)
    twitter_url = Property(str)
    updated_by_api_key = Property(str)
    url = Property(str)
    zipcode = Property(str)


@resource('manufacturer_images')
class ManufacturerImage(Model):
    caption = Property(str)
    default = Property(bool)
    id = Property(int)
    manufacturer_id = Property(int)
    url = Property(str)


@resource('option_sets')
class OptionSet(Model):
    id = Property(int)
    manufacturer_id = Property(int)
    name = Property(str)
    type = Property(str)


@resource('sales_channels')
class SalesChannel(Model):
    api_key_id = Property(int)
    bio = Property(str)
    city = Property(str)
    email = Property(str)
    facebook_url = Property(str)
    google_plus_url = Property(str)
    id = Property(int)
    isolated_image = Property(bool)
    linkedin_url = Property(str)
    logo_url = Property(str)
    other_image = Property(bool)
    phone = Property(str)
    phone_extension = Property(str)
    pinterest_url = Property(str)
    sales_channel_name = Property(str)
    setting_image = Property(bool)
    state = Property(str)
    street_address_1 = Property(str)
    street_address_2 = Property(str)
    twitter_url = Property(str)
    url = Property(str)
    visible = Property(bool)
    zipcode = Property(str)


@resource('sales_channel_preferences')
class SalesChannelPreference(Model):
    active = Property(bool)
    description_description = Property(str)
    id = Property(int)
    identity_name = Property(str)
    manufacturer_id = Property(int)
    pricing_dealer_price = Property(bool)
    pricing_minimum_internet_price = Property(bool)
    pricing_msrp = Property(bool)
    pricing_trade_price = Property(bool)
    pricing_wholesale = Property(bool)
    sales_channel_id = Property(int)
