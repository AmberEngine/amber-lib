from datetime import datetime
import os
import unittest
import sys

import mock

from .models import bases
from . import client


class Context(object):
    public = 'mwyclv6bac2lqn9artt1o88laq4muk88483opkp9dnv8289f8olqrxlx7b2s7q8'
    private = "sn4ikxumkpi5dqb0vwo1ujbi68uv3bvoak1p0xzgbzhg71v9p1sn7a2t49dh2tz"
    host = "http://example.com"
    port = "8080"


FAKE_DATE = datetime(2015, 11, 30, 22, 36, 52, 538755)
FAKE_DATE_FORMAT = datetime.isoformat(FAKE_DATE)

FAKE_HAL = {
    "_embedded": {
        "models": [
            {"_links": "first"},
            {"_links": "second"}
        ]
    },
    "_links": {},
    "total": 2
}

FAKE_HAL_THREE = {
    "_embedded": {
        "models": [
            {"_links": "first"},
            {"_links": "second"},
            {"_links": "third"}
        ]
    },
    "_links": {},
    "total": 3
}

class ContainerTest(unittest.TestCase):
    def add_test(self):
        hal = {
            "_embedded": {
                "models": [
                    {"_links": "third"},
                ]
            },
            "_links": {},
            "total": 1
        }

        ctn1 = client.Container(FAKE_HAL, bases.Model, Context())
        ctn2 = client.Container(hal, bases.Model, Context())

        ctn3 = ctn1 + ctn2

        self.assertEqual(len(ctn1.values), 2)
        self.assertEqual(len(ctn2.values), 1)

        self.assertEqual(len(ctn3.values), 3)
        self.assertEqual(ctn3[-1]._links, "third")

    def add_wrong_type_test(self):
        ctn1 = client.Container(FAKE_HAL, bases.Model, Context())
        self.assertRaises(TypeError, lambda: ctn1 + "foobar")

    def contains_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, Context())
        print("wtf")
        model = ctn[0]
        self.assertIn(model, ctn)
        self.assertNotIn("foobar", ctn)

    def delete_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        second = ctn[1]

        del ctn[1]

        self.assertEqual(len(ctn), 2)
        self.assertEqual(ctn[1]._links, "third")
        self.assertNotIn(second, ctn)

    def delete_invalid_index_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, Context())

        def delete_index():
            del ctn[100]
        self.assertRaises(IndexError, delete_index)

    def get_slice_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        self.assertEqual(len(ctn[:]), 3)
        self.assertEqual(len(ctn[0:2]), 2)
        self.assertEqual(len(ctn[0:3:2]), 2)

        self.assertEqual(ctn[0:2][1]._links, "second")


    def get_invalid_slice_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        self.assertEqual(len(ctn[1:500]), 2)
        self.assertEqual(len(ctn[100:1001]), 0)

    def get_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        self.assertEqual(ctn[0]._links, "first")
        self.assertEqual(ctn[1]._links, "second")
        self.assertEqual(ctn[-1]._links, "third")

    def get_invalid_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        self.assertRaises(IndexError, lambda: ctn[42])
        self.assertRaises(IndexError, lambda: ctn[-99])

    def get_invalid_index_type(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        self.assertRaises(TypeError, lambda: ctn["one"])
        self.assertRaises(TypeError, lambda: ctn[[{"":""}]])

    def iter_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        values = ctn.values
        count = 0

        for item in ctn:
            self.assertEqual(values[count], item)
            count += 1

        self.assertEqual(count, len(ctn))

    def iter_no_items_test(self):
        ctn = client.Container({}, bases.Model, Context())
        count = 0

        for item in ctn:
            count += 1

        self.assertEqual(count, 0)

    def le_api_test(self):
        ctn = client.Container({}, bases.Model, Context())
        self.assertTrue((ctn <= ctn).startswith("le"))

if __name__ == "__main__":
    unittest.main()
