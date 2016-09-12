from amber_lib import client, query
from amber_lib.models import primaries
from amber_lib.models.bases import Model, Property, resource


class Component(Model):
    """ A layer on top of Model for handling differences between models and
    Component models.
    """

    _pk = 'component_data_id'
    _resource = 'component'
    component_data_id = Property(int)
    parent_id = Property(int)
    product_guid = Property(str)
    parent_name = Property(str)
    product_id = Property(int)

    def delete(self, id_=None):
        """ Delete a component.
        """
        if id_ is not None:
            if self.is_valid() and self.pk() != id_:
                raise ValueError
            else:
                setattr(self, self._pk, id_)

        if self.is_valid():
            client.send(
                client.DELETE,
                self.ctx(),
                self.endpoint(),
                None
            )
        else:
            raise ValueError

        self.clear()
        return self

    def endpoint(self):
        """ Retrieve the endpoint URL for the current component.
        """
        loc = '/components/%s' % self._resource

        if not self.is_valid():
            return loc

        if isinstance(self.pk(), int) and self.pk() > 0:
            return loc + '/%d' % self.pk()

        raise ValueError

    def retrieve(self, id_):
        """ Retreive a component by ID.
        """
        setattr(self, self._pk, id_)
        payload = client.send(
            client.GET,
            self.ctx(),
            self.endpoint(),
            None,
        )

        self.clear()
        self.from_dict(payload)
        return self

    def save(self, data=None):
        """ Save the current data in the model to the API.
        """
        if data is not None:
            self.update(data)

        if self.is_valid():
            returned_dict = client.send(
                client.PUT,
                self.ctx(),
                self.endpoint(),
                self.to_dict()
            )
        else:
            returned_dict = client.send(
                client.POST,
                self.ctx(),
                self.endpoint(),
                self.to_dict()
            )

        self.clear()
        self.update(returned_dict)
        return self

    def form_schema(self):
        """ Retrieve the Schema for the """
        endpoint = '/form_schemas/components?name=%s' % self._resource
        response = client.send(client.GET, self.ctx(), endpoint, {})
        return response


@resource('audit')
class Audit(Component):
    date_added = Property(str)
    date_updated = Property(str)
    updated_by_api_key = Property(str)


@resource('apron')
class Apron(Component):
    clearance = Property(float)
    style = Property(str)
    edge_style = Property(str)


@resource('arm')
class Arm(Component):
    height = Property(float)
    style = Property(str)


@resource('base')
class Base(Component):
    depth = Property(float)
    diameter = Property(float)
    height = Property(float)
    width = Property(float)


@resource('box')
class Box(Component):
    depth = Property(float)
    height = Property(float)
    weight = Property(float)
    width = Property(float)
    quantity = Property(int)
    volume = Property(float)


@resource('brand')
class Brand(Component):
    brand = Property(primaries.Brand)
    brand_id = Property(int)


@resource('bulb')
class Bulb(Component):
    base = Property(str)
    quantity = Property(int)
    kind = Property(str)
    wattage = Property(int)
    shape = Property(str)


@resource('category')
class Category(Component):
    primary = Property(str)
    secondary = Property(str)
    tertiary = Property(str)


@resource('collection')
class Collection(Component):
    collection = Property(primaries.Collection)
    collection_id = Property(int)


@resource('com_col')
class COMCOL(Component):
    com = Property(float)
    col = Property(float)
    contrast_welt = Property(str)
    contrast_leather = Property(str)


@resource('construction_information')
class ConstructionInformation(Component):
    assembly_required = Property(bool)
    distressed_finish = Property(bool)
    finish = Property(str)
    hardware = Property(str)
    joinery_type = Property(str)
    material = Property(str)
    nail_type = Property(str)


@resource('cover')
class Cover(Component):
    cover_name = Property(str)
    content = Property(str)
    location = Property(str)
    color = Property(str)
    cover_type = Property(str)
    cleaning_code = Property(str)


@resource('covers')
class Covers(Component):
    cover_list = Property(Cover, True)
    quantity = Property(int)


@resource('cushion')
class Cushion(Component):
    depth = Property(float)
    fill = Property(str)
    height = Property(float)
    style = Property(str)
    width = Property(float)
    quantity = Property(int)


@resource('cushions')
class Cushions(Component):
    cushion_list = Property(Cushion, True)
    quantity = Property(int)


@resource('feature')
class Feature(Component):
    description = Property(str)


@resource('description')
class Description(Component):
    alternate = Property(str)
    designer = Property(str)
    feature_list = Property(Feature, True)
    primary = Property(str)
    retail = Property(str)
    color = Property(str)
    style = Property(str)


@resource('door')
class Door(Component):
    depth = Property(float)
    height = Property(float)
    opening = Property(float)
    width = Property(float)
    quantity = Property(int)


@resource('doors')
class Doors(Component):
    door_list = Property(Door, True)
    quantity = Property(int)


@resource('durability')
class Durability(Component):
    flammability = Property(str)
    martindale = Property(str)
    wyzenbeek = Property(str)


@resource('drawer')
class Drawer(Component):
    depth = Property(float)
    height = Property(float)
    width = Property(float)
    quantity = Property(int)
    construction = Property(str)
    glide_type = Property(str)


@resource('drawers')
class Drawers(Component):
    drawer_list = Property(Drawer, True)
    quantity = Property(int)


@resource('electrical')
class Electrical(Component):
    exterior_use = Property(bool)
    switch_type = Property(str)
    voltage = Property(float)


@resource('fiber')
class Fiber(Component):
    construction = Property(str)
    pile = Property(str)


@resource('flame')
class Flame(Component):
    burner_capacity = Property(float)
    burning_time = Property(float)
    fuel_type = Property(str)
    heat_output = Property(float)
    minimum_room_size = Property(float)


@resource('footboard')
class Footboard(Component):
    depth = Property(float)
    floor_clearance = Property(float)
    height = Property(float)
    width = Property(float)


@resource('footrest')
class Footrest(Component):
    height = Property(float)


@resource('foundation_information')
class FoundationInformation(Component):
    foundation_construction = Property(str)
    foundation_type = Property(str)
    number_of_pieces = Property(str)
    pieces_included = Property(str)
    size = Property(str)
    weight_capacity = Property(float)


@resource('frame')
class Frame(Component):
    back_rail_height = Property(float)
    height = Property(float)


@resource('glass')
class Glass(Component):
    kind = Property(str)


@resource('group')
class Group(Component):
    child_id = Property(int)
    quantity = Property(int)


@resource('groups')
class Groups(Component):
    group_list = Property(Group, True)

    def children(self, specific_kind=''):
       ids = [g.other_product_id for g in self.group_list]
       where = query.Predicate('id', query.within(ids))

       if specific_kind:
            specific_kind = specific_kind.lower()
            if specific_kind in ['kit', 'group', 'kit_piece', 'product']:
                where = query.And(
                    where,
                    query.Predicate(
                        'type',
                        query.equal(specific_kind)
                    )
                )
            else:
                raise Exception('Cannot use that specified kind of child')

       return Product(self.ctx()).query(filtering=where)


@resource('headboard')
class Headboard(Component):
    depth = Property(float)
    floor_clearance = Property(float)
    height = Property(float)
    width = Property(float)


@resource('identity')
class Identity(Component):
    alternate_name = Property(str)
    manufacturer_sku = Property(str)
    name = Property(str)
    source_url = Property(str)
    upc = Property(str)


@resource('image')
class Image(Component):
    caption = Property(str)
    category = Property(str)
    default = Property(bool)
    description = Property(str)
    full_size = Property(str)
    large_size = Property(str)
    medium_size = Property(str)
    thumbnail_size = Property(str)


@resource('images')
class Images(Component):
    image_list = Property(Image, True)


@resource('instruction')
class Instruction(Component):
    cleaning_directions = Property(str)
    installation_directions = Property(str)


@resource('interior_dimension')
class InteriorDimension(Component):
    depth = Property(float)
    height = Property(float)
    width = Property(float)


@resource('keyword')
class Keyword(Component):
    keywords = Property(str)


@resource('leather')
class Leather(Component):
    finish = Property(str)
    hide_size = Property(float)
    pattern_number = Property(str)
    kind = Property(str)


@resource('manufacturer')
class Manufacturer(Component):
    manufacturer = Property(primaries.Manufacturer)
    manufacturer_id = Property(int)


@resource('mattress_compliances')
class MattressCompliances(Component):
    certipur_us = Property(bool)
    cpsc_16_cfr_compliant = Property(bool)
    cpsia_compliant = Property(bool)
    global_organic_textile_standard = Property(bool)
    gsa_approved = Property(bool)
    greenguard = Property(bool)
    usda_certified_biobased_product_label = Property(bool)
    usda_organic = Property(bool)


@resource('mattress_features')
class MattressFeatures(Component):
    box_spring_recommended = Property(bool)
    commercial_use = Property(bool)
    cover_included = Property(bool)
    dust_mite_resistant = Property(bool)
    fire_resistant = Property(bool)
    handles = Property(bool)
    hypo_allergenic = Property(bool)
    mildew_resistant = Property(bool)
    non_toxic = Property(bool)
    no_flip = Property(bool)
    organic = Property(bool)
    removeable_cover = Property(bool)
    sleep_cool_foam = Property(bool)
    works_with_adjustable_base = Property(bool)
    ventilated = Property(bool)


@resource('mattress_information')
class MattressInformation:
    additional_materials = Property(str)
    coil_count = Property(str)
    coil_gauge = Property(str)
    coils_included = Property(bool)
    comfort_level = Property(str)
    core_construction = Property(str)
    cover_closure_type = Property(str)
    crown_height = Property(float)
    mattress_layer = Property(str)
    pocketed_coils = Property(bool)
    recommended_foundation = Property(str)
    size = Property(str)
    thickness = Property(float)
    top = Property(str)
    weight_capacity = Property(float)


@resource('mattress_specifications')
class MattressSpecifications:
    construction = Property(str)
    depth = Property(float)
    height = Property(float)
    size = Property(str)
    thickness = Property(float)
    width = Property(float)


@resource('option_set')
class OptionSet(Component):
    option_set_id = Property(int)
    option_set = Property(primaries.OptionSet)


@resource('option_sets')
class OptionSets(Component):
    option_set_list = Property(OptionSet, True)


@resource('ordering_information')
class OrderingInformation(Component):
    discontinued = Property(bool)
    force_multiples = Property(int)
    lead_time = Property(int)
    lead_time_unit = Property(str)
    minimum_quantity = Property(int)
    quick_ship = Property(bool)
    unit = Property(str)
    stock = Property(float)
    warranty_terms = Property(str)
    warranty_length = Property(str)


@resource('output')
class Output(Component):
    output_id = Property(int)


@resource('overall_dimension')
class OverallDimension(Component):
    depth = Property(float)
    max_depth = Property(float)
    diameter = Property(float)
    max_diameter = Property(float)
    height = Property(float)
    max_height = Property(float)
    width = Property(float)
    max_width = Property(float)
    volume = Property(float)


@resource('pattern')
class Pattern(Component):
    color = Property(primaries.MultiValueList)
    design_type = Property(primaries.MultiValueList)
    direction = Property(str)
    horizontal_repeat = Property(float)
    pattern_number = Property(str)
    scale = Property(str)
    vertical_repeat = Property(float)


@resource('pedestal')
class Pedestal(Component):
    diameter = Property(float)
    depth = Property(float)
    height = Property(float)
    width = Property(float)
    pedestal_type = Property(str)
    clearance_between_legs = Property(str)
    clearance_between_bases = Property(str)
    crossbands = Property(str)
    leg_style = Property(str)
    stretcher_style = Property(str)


@resource('pillow')
class Pillow(Component):
    width = Property(float)
    height = Property(float)
    quantity = Property(int)
    thickness = Property(float)


@resource('pillows')
class Pillows(Component):
    pillow_list = Property(Pillow, True)
    quantity = Property(int)


@resource('pricing')
class Pricing(Component):
    dealer_price = Property(int)
    internal_cost = Property(int)
    minimum_internet_price = Property(int)
    msrp = Property(int)
    trade_price = Property(int)
    wholesale = Property(int)


@resource('inventory')
class Inventory(Component):
    in_stock = Property(bool)
    limited_stock = Property(bool)
    planned_discontinued = Property(bool)
    discontinued = Property(bool)
    out_of_stock = Property(bool)


@resource('rug_construction')
class RugConstruction(Component):
    content = Property(str)
    backing = Property(str)
    construction = Property(primaries.MultiValueList)
    material = Property(primaries.MultiValueList)


@resource('rug_pattern')
class RugPattern(Component):
    custom_size = Property(bool)
    scale = Property(str)
    shape = Property(primaries.MultiValueList)
    color = Property(primaries.MultiValueList)
    style = Property(primaries.MultiValueList)


@resource('seat')
class Seat(Component):
    construction = Property(str)
    depth = Property(float)
    height = Property(float)
    width = Property(float)


@resource('shade')
class Shade(Component):
    depth = Property(float)
    diameter = Property(float)
    height = Property(float)
    material = Property(str)
    quantity = Property(int)
    kind = Property(str)
    width = Property(float)


@resource('shelf')
class Shelf(Component):
    depth = Property(float)
    width = Property(float)
    quantity = Property(int)
    thickness = Property(float)


@resource('shelves')
class Shelves(Component):
    quantity = Property(int)
    shelf_list = Property(Shelf, True)


@resource('shipping_information')
class ShippingInformation(Component):
    box_list = Property(Box, True)
    drop_ship = Property(bool)
    freight = Property(bool)
    notes = Property(str)
    ships_from = Property(str)
    standard = Property(bool)
    volume = Property(float)
    white_glove = Property(bool)
    country_of_origin = Property(str)


@resource('side_rail')
class SideRail(Component):
    floor_clearance = Property(float)
    length = Property(float)


@resource('suspension_point')
class SuspensionPoint(Component):
    canopy_depth = Property(float)
    canopy_diameter = Property(float)
    canopy_height = Property(float)
    canopy_width = Property(float)
    chain_length = Property(float)
    maximum_hanging_length = Property(float)
    minimum_hanging_length = Property(float)
    support_type = Property(str)
    wire_length = Property(float)


@resource('table_leaf')
class TableLeaf(Component):
    depth = Property(float)
    width = Property(float)
    quantity = Property(int)
    leaf_notes = Property(str)


@resource('table_leaves')
class TableLeaves(Component):
    quantity = Property(int)
    table_leaf_list = Property(TableLeaf, True)


@resource('textile')
class Textile(Component):
    content = Property(str)
    grade = Property(str)
    treatment = Property(str)
    usage = Property(primaries.MultiValueList)
    weave_type = Property(primaries.MultiValueList)
    width = Property(float)


@resource('weight')
class Weight(Component):
    weight = Property(float)


@resource('visibility')
class Visibility(Component):
    active = Property(bool)
    meets_posting_requirements = Property(bool)
