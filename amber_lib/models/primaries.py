import amberlib.models.base as base


class APIKey(base.Model):
    def __init__(self):
        self.id = ""
        self.name = ""
        self.public = ""
        self.private = ""
        self.type = ""
        self.manufacturer_id = ""
        self.sales_channel_id = ""


class Collection:
    pass


class Event:
    pass


class Export:
    pass


class Manufacturer:
    pass


class ManufacturerImage:
    pass


class OptionSet:
    pass


class Product:
    pass


class SalesChannel:
    pass
