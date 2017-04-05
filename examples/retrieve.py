""" Examples for how to retrieve resources.

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

    brand = ctx.brands.retrieve(1337)
    print(brands)

    prod = ctx.products.retrieve(4123)
    print(prod)

    prod = ctx.products.retrieve(4123, owner_type="channel_set", owner_id=32)
    print(prod) # print product which belongs to channel set, (instead of just the brand)


    mfr = ctx.manufacturers.retrieve(542)
    print(mfr.name)
    print(mfr.id)

if __name__ == "__main__":
    main()
