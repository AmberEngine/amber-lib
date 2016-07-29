from amber_lib.models.bases import Model, Property, resource
from amber_lib import client
from amber_lib.errors import MethodNotAllowed

@resource('api_keys')
class APIKey(Model):
    brand_id = Property(int)
    id = Property(int)
    kind = Property(str)
    manufacturer_id = Property(int)
    name = Property(str)
    private = Property(str)
    public = Property(str)
    role_name = Property(str)
    sales_channel_id = Property(int)
    token_secret = Property(str)


@resource('brands')
class Brand(Model):
    bio = Property(str)
    city = Property(str)
    date_added = Property(str)
    date_updated = Property(str)
    email = Property(str)
    facebook_url = Property(str)
    featured = Property(bool)
    google_plus_url = Property(str)
    id = Property(int)
    legal = Property(str)
    linkedin_url = Property(str)
    logo_url = Property(str)
    manufacturer_id = Property(int)
    name = Property(str)
    phone = Property(str)
    phone_extension = Property(str)
    pinterest_url = Property(str)
    restock_fee = Property(float)
    return_period = Property(int)
    returnable = Property(bool)
    state = Property(str)
    street_address_1 = Property(str)
    street_address_2 = Property(str)
    province = Property(str)
    country = Property(str)
    twitter_url = Property(str)
    updated_by_api_key = Property(str)
    url = Property(str)
    zipcode = Property(str)


@resource('categories')
class Categories(Model):
    primary = Property(str, True)
    secondary = Property(str, True)
    tertiary = Property(str, True)

    class Count(Model):
        primary_categories = Property(int)
        secondary_categories = Property(int)
        tertiary_categories = Property(int)
    count = Property(Count)
    total = Property(int)

    def delete(self):
        pass

    def save(self):
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
    id = Property(int)
    resource_name = Property(str)
    resource_action = Property(str)
    resource_id = Property(int)
    created_by_api_key = Property(str)
    date_created = Property(str)
    ip = Property(str)


@resource('exports')
class Export(Model):
    id = Property(int)
    user_email = Property(str)
    user_manufacturer_id = Property(int)
    product_ids = Property(int, True)
    url = Property(str)
    date_created = Property(str)
    date_exported = Property(str)
    mapping_id = Property(int)
    mapping_name = Property(str)
    message = Property(str)
    status = Property(str)


@resource('export_jobs')
class ExportJob(Model):
    export_id = Property(int)


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
    internal = Property(bool)
    legal = Property(str)
    linkedin_url = Property(str)
    logo_url = Property(str)
    name = Property(str)
    phone = Property(str)
    phone_extension = Property(str)
    pinterest_url = Property(str)
    restock_fee = Property(float)
    return_period = Property(int)
    returnable = Property(bool)
    state = Property(str)
    street_address_1 = Property(str)
    street_address_2 = Property(str)
    province = Property(str)
    country = Property(str)
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


class MultiValue(Model):
    component = Property(str)
    id = Property(int)
    value = Property(str)
    value_type = Property(str)


class MultiValueList(Model):
    multi_values = Property(int, True)
    accepted_values = Property(MultiValue, True)

@resource('options')
class Option(Model):
    class Nailhead(Model):
        id = Property(int)
        option_id = Property(int)
        finish = Property(str)
        height = Property(float)
        width = Property(float)
        depth = Property(float)
        diameter = Property(float)

    class Leather(Model):
        id = Property(int)
        option_id = Property(int)
        leather_type = Property(str)
        pattern_number = Property(str)
        hide_size = Property(float)
        average_thickness = Property(float)
        finish = Property(str)
        performance = Property(str)
        flammability = Property(str)
        cleaning_instructions = Property(str)
        grade = Property(str)

    class Hardware(Model):
        depth = Property(float)
        diameter = Property(float)
        finish = Property(str)
        height = Property(float)
        id = Property(int)
        option_id = Property(int)
        width = Property(float)

    class Textile(Model):
        id = Property(int)
        option_id = Property(int)
        content = Property(str)
        cleaning_instructions = Property(str)
        direction = Property(str)
        color = Property(str)
        design_type = Property(str)
        flammability = Property(str)
        grade = Property(str)
        horizontal_repeat = Property(float)
        martindale = Property(str)
        pattern_number = Property(str)
        scale = Property(str)
        treatment = Property(str)
        usage = Property(str)
        vertical_repeat = Property(float)
        weave_type = Property(str)
        width = Property(float)
        wyzenbeek = Property(str)

    class Trim(Model):
        id = Property(int)
        option_id = Property(int)
        color = Property(str)
        content = Property(str)
        height = Property(float)
        width = Property(float)
        depth = Property(float)
        diameter = Property(float)
        trim_type = Property(str)

    class Arm(Model):
        id = Property(int)
        option_id = Property(int)
        height = Property(float)
        width = Property(float)
        depth = Property(float)
        diameter = Property(float)
        style = Property(str)

    class Cushion(Model):
        id = Property(int)
        option_id = Property(int)
        height = Property(float)
        width = Property(float)
        depth = Property(float)
        diameter = Property(float)
        fill = Property(str)
        style = Property(str)
        cushion_type = Property(str)

    class Leg(Model):
        id = Property(int)
        option_id = Property(int)
        height = Property(float)
        width = Property(float)
        depth = Property(float)
        diameter = Property(float)
        style = Property(str)
        finish = Property(str)
        material = Property(str)

    class Skirt(Model):
        id = Property(int)
        option_id = Property(int)
        height = Property(float)
        style = Property(str)

    arm = Property(Arm)
    cushion = Property(Cushion)
    default = Property(bool)
    description = Property(str)
    hardware = Property(Hardware)
    id = Property(int)
    image = Property(str)
    kind = Property(str)
    leather = Property(Leather)
    leg = Property(Leg)
    nail_head = Property(Nailhead)
    name = Property(str)
    number = Property(str)
    option_set_id = Property(int)
    skirt = Property(Skirt)
    surcharge = Property(int)
    textile = Property(Textile)
    trim = Property(Trim)


@resource('option_sets')
class OptionSet(Model):
    id = Property(int)
    manufacturer_id = Property(int)
    name = Property(str)
    kind = Property(str)
    option_list = Property(Option, True)


@resource('retailers')
class Retailer(Model):
    bio = Property(str)
    city = Property(str)
    country = Property(str)
    date_added = Property(str)
    date_updated = Property(str)
    email = Property(str)
    facebook_url = Property(str)
    google_plus_url = Property(str)
    id = Property(int)
    legal = Property(str)
    linkedin_url = Property(str)
    logo_url = Property(str)
    name = Property(str)
    phone = Property(str)
    phone_extension = Property(str)
    pinterest_url = Property(str)
    province = Property(str)
    state = Property(str)
    street_address_1 = Property(str)
    street_address_2 = Property(str)
    twitter_url = Property(str)
    updated_by_api_key = Property(str)
    url = Property(str)
    website = Property(str)
    zipcode = Property(str)


@resource('channels')
class Channel(Model):
    id = Property(int)
    channel_type = Property(str)
    variety = Property(str)
    retailer_id = Property(int)
    name = Property(str)


@resource('channel_sets')
class ChannelSet(Model):
    id = Property(int)
    channel_ids = Property(int, True)
    date_added = Property(str)
    channel_ids = Property(int, True)
    name = Property(str)
    last_update_sent = Property(str)
    manufacturer_id = Property(int)
    brand_id = Property(int)
    msrp = Property(int)
    msrp_enabled = Property(bool)
    trade_price = Property(int)
    trade_price_enabled = Property(bool)
    wholesale_price = Property(int)
    wholesale_price_enabled = Property(bool)
    minimum_internet_price = Property(int)
    minimum_internet_price_enabled = Property(bool)
    dealer_price = Property(int)
    dealer_price_enabled = Property(bool)


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
    name = Property(str)
    setting_image = Property(bool)
    state = Property(str)
    street_address_1 = Property(str)
    street_address_2 = Property(str)
    twitter_url = Property(str)
    url = Property(str)
    visible = Property(bool)
    zipcode = Property(str)

    def related_product_ids(self):
        """ related_product_ids will return a dictionary containing both a
        list of product id (in the "product_ids" attribute) and a count of
        the total number of product IDs returned.
        """
        if not self.is_valid():
            raise Exception('Sales Channel is not valid')

        payload = client.send(
            client.GET,
            self.ctx(),
            '/relations',
            None,
            sales_channel_id=self.pk()
        )

        return payload


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
