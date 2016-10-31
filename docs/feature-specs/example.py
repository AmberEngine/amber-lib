import amber_lib as lib

lib.Product(conn).retrieve("123142", embedded=[], ignore=[])

# if no embedded, nothing gets embedded. That includes skipping components
prod = conn.product().retrieve(
    "123142",
    embedded=["component.*"],
    ignore=["options", "brand", "components.shipping_information.boxes"]
)

id_filter = Predicate("id", "in", [1, 2, 3, 4, 5])
added_filter = Predicate("components.audit.date_added", ">", time.Now())
updated_filter = Predicate("components.audit.date_updated", ">", time.Now())
brand_filter = Predicate("components.brand.brand.id", "not in", [1337, 42])

brand = prod.embedded.brands[0]
brand = prod.components.brand.brand

conn.component.identity()

res = conn.listing.product().retrieve(
    batch_size=5,
    terms="foobar",
    limit=2,
    offset=3,
    filtering=And(id_filter, Or(date_added, date_updated), brand_filter),
    embedded=["components.*"],
    ignore=["options", "brand", "components.shipping_information.boxes"]
)


class Product(Base):
    # change _embedded to embedded, _links to links
    __internal_dict = json_reponse

    def __getattr__(self, key):
        pass

    def __del__(self, key):
        del self.__internal_dict[key]


del prod.images.image_list[0]
prod.save()



prod = conn.product().retrieve("2m40a2m4", version_id=123124124)
prod = conn.product().retrieve("5n03m5maam2m43gmsm35m23af3gsae4")

prods = conn.listing.product()

prod = lib.Product(conn)

prod = conn.Product()
listing = conn.listing.products()
ident = conn.component.identity()


conn.component.identity()

conn.listing.brand()
conn.listing.channel()
conn.component.identity()


lib.primary.Product()


p = conn.product()
p.affordances()
p.create()
p.delete()
p.refresh() -> p.retrieve()
p.relate(...)
p.retrieve()
p.unrelate(...)
p.update()

p.pk()
p.schema()

p.to_dict()
p.to_json()

p.from_dict()
p.from_json()

listing = conn.ProductListing().retrieve()
prod = conn.Product().retrieve(1).update(data)

prod2 = prod.retrieve()
prod.create()
prod.update()
prod.delete()


prods = []
prodList = conn.ProductListing.retrieve()

while prodList.is_valid():
    prods.append(prodList.embedded.products)
    prodList = prodList.next()

prods = []
prodList = conn.ProductListing.retrieve()

for listing in prodList.all():
    prods.append(listing.embedded.products)


conn.ProductListing.retrieve()
                .next()
                .prev()
                .first()
                .last()

conn.ProductListing.retrieve(
    batch_size=100,
    terms="",
    limit=0,
    offset=0,
    filtering=None,
    embedded=[],
    ignore=[]
)


