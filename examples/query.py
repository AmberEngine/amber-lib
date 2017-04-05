""" Examples for how to query resources.

NOTE: This is NOT runnable code. You need to update the public and private
values of the Context. You may also need to adjust function args to properly
work with your actual dataset.
"""

from amber_lib import Context, query


def main():
    ctx = Context(
        host="http://api.amberengine.com",
        port="80",
        public="your_public_key_here",
        private="your_private_key_here"
    )

    opt_sets = ctx.option_sets.query()
    for opt_set in opt_sets.embedded.option_sets:
        print(opt_set) # Print out each provided option set.

    prods = ctx.products.query()
    for prod in prods.embedded.products:
        print(prod) # Print out each individual product.

    print(prods.embedded) # Things other than Product may be embedded.
    print(len(prods)) # Will be the max batch size the API will return.

    prods = ctx.products.query(limit=5, offset=10)
    print(len(prods)) # Will be 5.

    prods = prods.next() # Affordances are NOT mutable. Always returns a new instance.
    print(len(prods)) # Still 5. This is the next 10 products.

    sparse_prods = ctx.products.query(fields="identity")
    print(sparse_prods.embedded.products[0].identity) # {"name": "...", "sku": "..."}
    print(sparse_prods.embedded.products[0].ordering_information) # Attribute error

    predicate = query.Predicate("id", "in", [1, 2, 3, 4])
    prods = ctx.products.query(body={"filtering": predicate})
    print(prods) # Only contains products which have the ID: 1, 2, 3, or 4.


    predicate = query.Predicate("shipping_information.volume", ">", 54.32)
    prods = ctx.products.query(body={"filtering": predicate})
    print(prods) # Only contains products which have s shipping info volume greater than 54.32


if __name__ == "__main__":
    main()
