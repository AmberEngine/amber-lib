import amberlib.models.bases.Model as Model
import amberlib.models.base.Property as Property

class APIKey(Model):
    attributes = {
        'id': Property(int),
        'name': Property(str),
        'public': Property(str),
        'private': Propery(str),
        'type': Property(str),
        'manufacturer_id': Property(int),
        'sales_channel_id': Property(int)
    }


class Collection(Model):
    attributes = {
        'id': Property(int),
        'manufacturer_id': Property(int),
        'description': Property(str),
        'designed_by': Property(str)
    }


class Event(Model):
    attributes = {
        'id': Property(int),
        'name': Property(str),
        'message': Property(str),
        'object_id': Property(int),
        'object_type': Property(str),
        'date_time': Property(str)
    }


class Export:
    pass


class Manufacturer:
    attributes = {
        'id': Property(int),
        'name': Property(str),
        'bio': Property(str),
        'url': Property(str),
        'logo_url': Property(str),
        'date_added': Property(str),
        'date_updated': Property(str),
        'date_profile_complete': Property(str),
        'update_by_api_key': Property(str),
        'active': Property(bool),
        'city': Property(str),
        'email': Property(str),
        'facebook_url': Property(str),
        'google_plus_url': Property(str),
        'legal': Property(str)
    }


class ManufacturerImage(Model):
    attributes = {
        'id': Property(int),
        'manufacturer_id': Property(int),
        'default': Property(bool),
        'caption': Property(str),
        'url': Property(str)
    }


class OptionSet(Model):
    attributes = {
        'id': Property(int),
        'manufacturer_id': Property(int),
        'name': Property(str),
        'type': Property(str)
    }


class Product(Model):
    attributes = {
        'id': Property(int),
        'assemblage': Property(models.primaries.Assemblage),
        'arm': Property(models.components.Arm),
        'audit': Property(models.components.Audit),
        'category': Property(models.components.Category),
        'collection': Property(models.components.Collection),
        'construction_information': Property(
            models.components.ConstructionInformation
        ),
        'cushion': Property(models.components.Cushion),
        'description': Property(models.components.Description),
        'door': Property(models.components.Door),
        'drawer': Property(models.components.Drawer),
        'durability': Property(models.components.Durability),
        'footrest': Property(models.components.Footrest),
        'identity': Property(models.components.Identity),
        'image': Property(models.components.Image),
        'instructions': Property(models.components.Instructions),
        'manufacturer': Property(models.components.Manufacturer),
        'option': Property(models.components.Option),
        'ordering_information': Property(
            models.components.OrderingInformation
        ),
        'pattern': Property(models.components.Pattern),
        'pricing': Property(models.components.Pricing),
        'pedestal': Property(models.components.Pedestal),
        'pillow': Property(models.components.Pillow),
        'promotional_tags': Property(models.components.PromotionalTags),
        'overall_dimensions': Property(models.components.OverallDimensions),
        'seat': Property(models.components.Seat),
        'shelf': Property(models.components.Shelf),
        'shipping_information': Property(
            models.components.ShippingInformation
        ),
        'table_leaf': Property(models.components.TableLeaf),
        'textile': Property(models.components.Textile),
        'visibility': Property(models.components.Visibility),
        'weight': Property(models.components.Weight)
    }


class SalesChannel(Model):
    attributes = {
        'id': Property(int),
        'api_key_id': Property(int),
        'visible': Property(bool),
        'name': Property(str),
        'bio': Property(str),
        'url': Property(str),
        'logo_url': Property(str),
        'phone': Property(str),
        'extension': Property(str),
        'street_address_1': Property(str),
        'street_address_2': Property(str),
        'city': Property(str),
        'state': Property(str),
        'zipcode': Property(str),
        'facebook_url': Property(str),
        'google_plus_url': Property(str),
        'linkedin_url': Property(str),
        'pinterest_url': Property(str),
        'twitter_url': Property(str),
        'setting_image': Property(bool),
        'isolated_image': Property(bool),
        'other_image': Property(bool)
    }


class SalesChannelPreference(Model):
    attributes = {
        'id': Property(int),
        'manufacturer_id': Property(int),
        'sales_channel_id': Property(int),
        'active': Property(bool),
        'description_description': Property(str),
        'identity_name': Property(str),
        'pricing_dealer_price': Property(bool),
        'pricing_minimum_internet_price': Property(bool),
        'pricing_msrp': Property(bool),
        'pricing_trade_price': Property(bool),
        'pricing_wholesale': Property(bool)
        }
