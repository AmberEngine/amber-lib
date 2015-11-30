import amberlib.models.bases as bases


class Cushion(bases.Component):
    attributes = {
        "fill": Property(str),
        "style": Property(str),
        "width": Property(float),
        "depth": Property(float),
        "height": Property(float)
    }


class Door(base.Component):
    attributes = {
        "width": Property(float),
        "depth": Property(float),
        "height": Property(float),
        "opening": Property(float)
    }


class Drawer(base.Component):
    attributes = {
        "width": Property(float),
        "depth": Property(float),
        "height": Property(float)
    }


class Image(bases.Component):
    attributes = {
        "default": Property(bool),
        "category": Property(str),
        "caption": Property(str),
        "fullsize": Property(str),
        "large_size": Property(str),
        "medium_size": Property(str),
        "thumbnail_size": Property(str)
    }


class OptionSet(bases.Component):
    attributes = {
        "option_set_id": Property(int)
    }


class Pillow(bases.Component):
    attributes = {
        "width": Property(float),
        "height": Property(float),
        "depth": Property(float)
    }


class Shelf(base.Component):
    attributes = {
        "width": Property(float),
        "height": Property(float),
        "depth": Property(float)
    }


class ShippingInformation(bases.Component):
    attributes = {
        "weight": Property(float),
        "width": Property(float),
        "height": Property(float),
        "depth": Property(float)
    }


class TableLeaf(bases.Component):
    attributes = {
        "width": Property(float),
        "depth": Property(float)
    }
