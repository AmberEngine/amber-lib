""" Examples for how to query resources.

NOTE: This is NOT runnable code. You need to update the public and private
values of the Context. You may also need to adjust function args to properly
work with your actual dataset.
"""

from amber_lib import Context, query
import time

def main():
    ctx = Context(
        host="http://api.amberengine.dev",
        #host="http://ec2-54-145-166-215.compute-1.amazonaws.com/",
        port="80",
        public='8abebf3699d76c1707cc192a1627a100888b873e567c85765c0ce52d51129523',
        private='b8c056bc53fa4dcd3665978da53beab6e24a5b64b33f2f625c3c51fb63858130',
        request_attempts=1
    )

    start = time.time()
    channel_set = ctx.channel_sets.create(body={
        "owner_type": "brand",
        "owner_id": 24,
        "name": "benchmark channel set test",
        "is_dirty": False,
    })
    print("Create Channel Set: %s seconds" % (time.time() - start))


    start = time.time()
    products = ctx.products.query(owner_type="brand", owner_id=24, limit=5)
    print("Queried for %i products: %s seconds" % (products.count, time.time() - start))

    start = time.time()
    res = channel_set._links.relate.products(body={
        "channel_sets": [channel_set.id],
        "products": {
            "ids": [p.id for p in products._embedded.products],
            "owner_type": "brand",
            "owner_id": 24
        }
    })
    print("Related %i products to Channel Set #%i: %s seconds" % (products.count, channel_set.id, time.time() - start))

    print(res)


if __name__ == "__main__":
    main()
