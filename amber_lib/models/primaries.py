from amber_lib.models.bases import Model, Property, resource
from amber_lib import client
from amber_lib.errors import MethodNotAllowed


@resource('api_keys')
class APIKey(Model):
    id = Property(int)
    manufacturer_id = Property(int)
    name = Property(str)
    private = Property(str)
    public = Property(str)
    sales_channel_id = Property(int)
    kind = Property(str)
    role_name = Property(str)


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


@resource('event')
class Event(Model):
    date_time = Property(str)
    id = Property(int)
    message = Property(str)
    name = Property(str)
    object_id = Property(int)
    object_type = Property(str)


@resource('moments')
class Moment(Model):
    id = Property(int)
    resource_name = Property(str)
    resource_action = Property(str)
    created_by_api_key = Property(int)
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

    class Hardware(Model):
        id = Property(int)
        option_id = Property(int)
        finish = Property(str)
        height = Property(float)
        width = Property(float)
        depth = Property(float)
        diameter = Property(float)

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

    id = Property(int)
    option_set_id = Property(int)
    number = Property(str)
    name = Property(str)
    description = Property(str)
    default = Property(bool)
    image = Property(str)
    surcharge = Property(int)
    kind = Property(str)
    extended_data = Property((Nailhead, Leather, Hardware, Textile, Trim))

    def from_dict(self, dict_):
        """ Update the internal dictionary for the instance using the
        key-value pairs contained within the provided dictionary.
        """
        if 'kind' in dict_:
            self.kind = dict_['kind']
        def explode_dict(obj, exp_dict):
            for key, val in exp_dict.items():
                attr = object.__getattribute__(obj, key)

                if isinstance(val, dict):
                    if not isinstance(attr, dict):
                        type_ = obj.kind
                        if not getattr(obj, key):
                            inst = None

                            if type_ == "nailhead":
                                inst = Option.Nailhead(obj.ctx())
                            elif type_ == "leather":
                                inst = Option.Leather(obj.ctx())
                            elif type_ == "hardware":
                                inst = Option.Hardware(obj.ctx())
                            elif type_ == "textile":
                                inst = Option.Textile(obj.ctx())
                            elif type_ == "trim":
                                inst = Option.Trim(obj.ctx())
                            elif type_ == "finish":
                                pass  # because finish has no extra fields
                            if inst is None:
                                val = None
                            else:
                                val = inst.from_dict(val)
                        else:
                            val = getattr(obj, key).from_dict(val)
                elif isinstance(val, list):
                    list_ = []
                    for el in val:
                        if isinstance(el, dict):
                            inst = attr.kind(obj.ctx())
                            el = inst.from_dict(el)
                        list_.append(el)
                    val = list_
                setattr(obj, key, val)
            return obj
        return explode_dict(self, dict_)



@resource('option_sets')
class OptionSet(Model):
    id = Property(int)
    manufacturer_id = Property(int)
    name = Property(str)
    kind = Property(str)
    option_list = Property(Option, True)


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
            raise Exception("Sales Channel is not valid")

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
