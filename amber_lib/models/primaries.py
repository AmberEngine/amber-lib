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
    retailer_id = Property(int)
    role_name = Property(str)
    sales_channel_id = Property(int)
    token_secret = Property(str)

# This class must come before Brand and Retailer because it is used in both of
# those classes.
@resource('brand_retailer_relations')
class BrandRetailerRelation(Model):
    brand_id = Property(int)
    id = Property(int)
    retailer_id = Property(int)


@resource('brand_channel_relations')
class BrandChannelRelation(Model):
    brand_id = Property(int)
    channel_id = Property(int)
    id = Property(int)


@resource('retailer_channel_relations')
class RetailerChannelRelation(Model):
    channel_id = Property(int)
    id = Property(int)
    retailer_id = Property(int)


@resource('brands')
class Brand(Model):
    accessible_channels = Property(BrandChannelRelation, True)
    active = Property(bool)
    bio = Property(str)
    city = Property(str)
    country = Property(str)
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
    province = Property(str)
    restock_fee = Property(float)
    retailer_relation = Property(BrandRetailerRelation, True)
    return_period = Property(int)
    returnable = Property(bool)
    state = Property(str)
    street_address_1 = Property(str)
    street_address_2 = Property(str)
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
    brand_id = Property(int)
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
    resource_owner_type = Property(str)
    resource_id = Property(int)
    created_by_api_key = Property(str)
    date_created = Property(str)
    ip = Property(str)


@resource('exports')
class Export(Model):
    date_created = Property(str)
    date_exported = Property(str)
    id = Property(int)
    mapping_id = Property(int)
    mapping_name = Property(str)
    message = Property(str)
    output_id = Property(int)
    parent = Property(bool)
    product_ids = Property(str, True)
    status = Property(str)
    url = Property(str)
    user_email = Property(str)
    user_manufacturer_id = Property(int)
    user_retailer_id = Property(int)


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
    nailhead = Property(Nailhead)
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
    brand_id = Property(int)
    manufacturer_id = Property(int)
    name = Property(str)
    kind = Property(str)
    option_list = Property(Option, True)


@resource('pushes')
class Push(Model):
    channel_set_id = Property(int)
    end_timestamp = Property(str)
    id = Property(int)
    start_timestamp = Property(str)


@resource('retailers')
class Retailer(Model):
    accessible_channels = Property(RetailerChannelRelation, True)
    bio = Property(str)
    brand_relation = Property(BrandRetailerRelation, True)
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


    def set_relation(self, bool_, obj, refresh=True):
        """ Create or remove a relation between the current model and a
        different model.
        """
        #self.save()
        res1 = self._resource
        print(obj)
        res2 = obj._resource

        if res2 != "products":
            payload = client.send(
                client.POST if bool_ is True else client.DELETE,
                self.ctx(),
                '/relations',
                **{
                    res1: self.pk(),
                    res2: obj.pk()
                }
            )
        else:
            payload = client.send(
                client.POST if bool_ is True else client.DELETE,
                self.ctx(),
                '/relations',
                json_data={
                    "products": {
                        "owner_id": obj.owner_id,
                        "owner_type": obj.owner_type,
                        "ids": [obj.pk()]
                    },
                    "retailers": [self.pk()]
                },
                **{
                    res1: self.pk(),
                    res2: obj.pk()
                }
            )
        # Dear Future Dev, if you're wondering why changes are disappearing
        # when relate/unrelate calls are made then this line is why, but
        # without it then relate/unrelate changes disappear on save calls.
        if refresh:
            obj.refresh()
            self.refresh()


    def set_relation_multiple(self, bool_, objs, refresh=True):
        """ Create or remove a relation between the current model and a
        different model.
        """
        #self.save()
        res1 = self._resource
        if len(objs) == 0:
            raise Exception("Must provide at least one object to relate to.")
        if not isinstance(objs, (list, client.Container)):
            raise Exception("Must provide a list of objects to relate to.")

        res2 = objs[0]._resource

        if res2 != "products":
            payload = client.send(
                client.POST if bool_ is True else client.DELETE,
                self.ctx(),
                '/relations',
                **{
                    res1: self.pk(),
                    res2: ",".join([str(obj.pk()) for obj in objs])
                }
            )
        else:
            payload = client.send(
                client.POST if bool_ is True else client.DELETE,
                self.ctx(),
                '/relations',
                json_data={
                    "products": {
                        "owner_id": objs[0].owner_id,
                        "owner_type": objs[0].owner_type,
                        "ids": [r.pk() for r in objs]
                    },
                    "retailers": [self.pk()]
                },
                **{
                    res1: self.pk(),
                    res2: objs[0].pk()
                }
            )
        # Dear Future Dev, if you're wondering why changes are disappearing
        # when relate/unrelate calls are made then this line is why, but
        # without it then relate/unrelate changes disappear on save calls.
        if refresh:
            for obj in objs:
                obj.refresh()
            self.refresh()


@resource('channels')
class Channel(Model):
    id = Property(int)
    channel_type = Property(str)
    export_id = Property(int)
    variety = Property(str)
    retailer_id = Property(int)
    name = Property(str)

    def set_relation(self, bool_, obj, refresh=True):
        """ Create or remove a relation between the current model and a
        different model.
        """
        #self.save()
        res1 = self._resource
        print(obj)
        res2 = obj._resource

        if res2 != "products":
            payload = client.send(
                client.POST if bool_ is True else client.DELETE,
                self.ctx(),
                '/relations',
                **{
                    res1: self.pk(),
                    res2: obj.pk()
                }
            )
        else:
            payload = client.send(
                client.POST if bool_ is True else client.DELETE,
                self.ctx(),
                '/relations',
                json_data={
                    "products": {
                        "owner_id": obj.owner_id,
                        "owner_type": obj.owner_type,
                        "ids": [obj.pk()]
                    },
                    "channels": [self.pk()]
                },
                **{
                    res1: self.pk(),
                    res2: obj.pk()
                }
            )
        # Dear Future Dev, if you're wondering why changes are disappearing
        # when relate/unrelate calls are made then this line is why, but
        # without it then relate/unrelate changes disappear on save calls.
        if refresh:
            obj.refresh()
            self.refresh()


    def set_relation_multiple(self, bool_, objs, refresh=True):
        """ Create or remove a relation between the current model and a
        different model.
        """
        #self.save()
        res1 = self._resource
        if len(objs) == 0:
            raise Exception("Must provide at least one object to relate to.")
        if not isinstance(objs, (list, client.Container)):
            raise Exception("Must provide a list of objects to relate to.")

        res2 = objs[0]._resource

        if res2 != "products":
            payload = client.send(
                client.POST if bool_ is True else client.DELETE,
                self.ctx(),
                '/relations',
                **{
                    res1: self.pk(),
                    res2: ",".join([str(obj.pk()) for obj in objs])
                }
            )
        else:
            payload = client.send(
                client.POST if bool_ is True else client.DELETE,
                self.ctx(),
                '/relations',
                json_data={
                    "products": {
                        "owner_id": objs[0].owner_id,
                        "owner_type": objs[0].owner_type,
                        "ids": [r.pk() for r in objs]
                    },
                    "channels": [self.pk()]
                },
                **{
                    res1: self.pk(),
                    res2: objs[0].pk()
                }
            )
        # Dear Future Dev, if you're wondering why changes are disappearing
        # when relate/unrelate calls are made then this line is why, but
        # without it then relate/unrelate changes disappear on save calls.
        if refresh:
            for obj in objs:
                obj.refresh()
            self.refresh()


@resource('channel_pushes')
class ChannelPush(Model):
    channel_id = Property(int)
    channel_set_id = Property(int)
    end_timestamp = Property(str)
    id = Property(int)
    product_guids = Property(str, True)
    product_ids = Property(int, True)
    push_id = Property(int)
    start_timestamp = Property(str)


@resource('channel_sets')
class ChannelSet(Model):
    channel_ids = Property(int, True)
    date_added = Property(str)
    dealer_price = Property(int)
    dealer_price_enabled = Property(bool)
    id = Property(int)
    is_dirty = Property(bool)
    last_update_sent = Property(str)
    minimum_internet_price = Property(int)
    minimum_internet_price_enabled = Property(bool)
    msrp = Property(int)
    msrp_enabled = Property(bool)
    name = Property(str)
    owner_id = Property(int)
    owner_type = Property(str)
    trade_price = Property(int)
    trade_price_enabled = Property(bool)
    wholesale_price = Property(int)
    wholesale_price_enabled = Property(bool)

    def set_relation(self, bool_, obj, refresh=True):
        """ Create or remove a relation between the current model and a
        different model.
        """
        #self.save()
        res1 = self._resource
        res2 = obj._resource

        if res2 != "products":
            payload = client.send(
                client.POST if bool_ is True else client.DELETE,
                self.ctx(),
                '/relations',
                **{
                    res1: self.pk(),
                    res2: obj.pk()
                }
            )
        else:
            payload = client.send(
                client.POST if bool_ is True else client.DELETE,
                self.ctx(),
                '/relations',
                json_data={
                    "products": {
                        "owner_id": obj.owner_id,
                        "owner_type": obj.owner_type,
                        "ids": [obj.pk()]
                    },
                    "channel_sets": [self.pk()]
                },
                **{
                    res1: self.pk(),
                    res2: obj.pk()
                }
            )
        # Dear Future Dev, if you're wondering why changes are disappearing
        # when relate/unrelate calls are made then this line is why, but
        # without it then relate/unrelate changes disappear on save calls.
        if refresh:
            obj.refresh()
            self.refresh()


    def set_relation_multiple(self, bool_, objs, refresh=True):
        """ Create or remove a relation between the current model and a
        different model.
        """
        #self.save()
        res1 = self._resource
        if len(objs) == 0:
            raise Exception("Must provide at least one object to relate to.")
        if not isinstance(objs, (list, client.Container)):
            raise Exception("Must provide a list of objects to relate to.")

        res2 = objs[0]._resource

        if res2 != "products":
            payload = client.send(
                client.POST if bool_ is True else client.DELETE,
                self.ctx(),
                '/relations',
                **{
                    res1: self.pk(),
                    res2: ",".join([str(obj.pk()) for obj in objs])
                }
            )
        else:
            payload = client.send(
                client.POST if bool_ is True else client.DELETE,
                self.ctx(),
                '/relations',
                json_data={
                    "products": {
                        "owner_id": objs[0].owner_id,
                        "owner_type": objs[0].owner_type,
                        "ids": [r.pk() for r in objs]
                    },
                    "channel_sets": [self.pk()]
                },
                **{
                    res1: self.pk(),
                    res2: objs[0].pk()
                }
            )
        # Dear Future Dev, if you're wondering why changes are disappearing
        # when relate/unrelate calls are made then this line is why, but
        # without it then relate/unrelate changes disappear on save calls.
        if refresh:
            for obj in objs:
                obj.refresh()
            self.refresh()


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
