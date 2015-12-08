from datetime import datetime
import math
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

    def len_total_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        self.assertEqual(len(ctn), 3)

    def len_empty_test(self):
        ctn = client.Container({}, bases.Model, Context())
        self.assertEqual(len(ctn), 0)

    def len_values_test(self):
        ctn = client.Container({}, bases.Model, Context())
        class Length:
            def __len__(self):
                return 42
        ctn.values = Length()
        self.assertEqual(len(ctn), 42)

    def pow_test(self):
        ctn = client.Container({}, bases.Model, Context())
        self.assertTrue('Mario' in ctn ** 42)

    def reversed_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        values = ctn[:]

        reversed_ctn = reversed(ctn)
        for i in range(len(reversed_ctn)):
            self.assertEqual(reversed_ctn[i], values[len(values) - i -1])

    def setitem_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        new_model = bases.Model({})
        new_model._links = "fourth"

        ctn[2] = new_model

        self.assertEqual(len(ctn), 3)
        self.assertEqual(ctn[-1]._links, "fourth")

    def setitem_invalid_range_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        new_model = bases.Model({})
        new_model._links = "fourth"

        def temp():
            ctn[42] = new_model
        self.assertRaises(IndexError, temp)

    def all_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        self.assertEqual(ctn[:].values, ctn._Container__all().values)

    def dunder_append_container_test(self):
        ctn1 = client.Container(FAKE_HAL, bases.Model, Context())
        ctn2 = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        ctn3 = client.Container({}, bases.Model, Context())

        expected = len(ctn1) + len(ctn2) + len(ctn3)

        ctn1._Container__append(ctn2)
        ctn1._Container__append(ctn3)
        self.assertEqual(len(ctn1), expected)

    def dunder_append_list_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, Context())
        models = [bases.Model({}), bases.Model({})]

        expected = len(ctn) + len(models)

        ctn._Container__append(models)
        self.assertEqual(len(ctn), expected)

    def dunder_append_item_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, Context())

        expected = len(ctn) + 1

        ctn._Container__append(bases.Model({}))
        self.assertEqual(len(ctn), expected)

    @mock.patch('amber_lib.client.Container._Container__all')
    def finish_it_test(self, mock_all):
        ctn = client.Container(FAKE_HAL, bases.Model, Context())
        ctn.total = 500
        ctn._Container__finish_it()

        mock_all.assert_called_with()

    @mock.patch('amber_lib.client.Container._Container__all')
    def finish_it_ignored_test(self, mock_all):
        ctn = client.Container(FAKE_HAL, bases.Model, Context())
        ctn._Container__finish_it()

        mock_all.assert_not_called()

    def dunder_get_invalid_negative_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        too_far_under = len(ctn) * -1
        self.assertRaises(IndexError, lambda: ctn._Container__get(too_far_under))

    def dunder_get_valid_negative_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        model = ctn[2]

        self.assertEqual(ctn._Container__get(-1), model)

    def dunder_get_invalid_positive_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        self.assertRaises(IndexError, lambda: ctn._Container__get(len(ctn)))

    def dunder_get_positive_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        self.assertEqual(ctn._Container__get(0)._links, "first")

    @mock.patch('amber_lib.client.Container._Container__next')
    def dunder_get_use_next_test(self, mock_next):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        mock_next.return_value = False

        ctn.total = 5
        def next_values():
            ctn.values[3] = "fourth"
            ctn.values[4] = "fifth"
        mock_next.side_effect = next_values

        self.assertEqual(ctn._Container__get(4), "fifth")
        mock_next.assert_called_with()



    @mock.patch('amber_lib.client.Container._Container__previous')
    def dunder_get_use_previous_test(self, mock_previous):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        mock_previous.return_value = False

        del ctn.values[0]
        ctn.offset = 2
        ctn.total = 5
        def prev_values():
            ctn.values[0] = "first index"
            ctn.values[1] = "second"
            ctn.offset = 0
        mock_previous.side_effect =  prev_values

        self.assertEqual(ctn._Container__get(0), "first index")
        mock_previous.assert_called_with()

    def dunder_next_no_hal_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        ctn.hal = None
        self.assertFalse(ctn._Container__next())

        ctn.hal = {}
        self.assertFalse(ctn._Container__next())

    @mock.patch('amber_lib.client.send')
    @mock.patch('amber_lib.client.Container._Container__append')
    def dunder_next_test(self, mock_append, mock_send):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        ctn.hal = {"next": {"href": "http://example.com/next"}}

        embedded = {"models": [0, 1, 2, 3]}
        hal_return = {"_embedded": embedded}

        mock_send.return_value = hal_return

        ctn._Container__next()

        self.assertTrue(mock_send.called)
        mock_append.assert_called_with(embedded['models'])

    def dunder_prepend_container_test(self):
        ctn1 = client.Container(FAKE_HAL, bases.Model, Context())
        ctn2 = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        ctn3 = client.Container({}, bases.Model, Context())

        expected = len(ctn1) + len(ctn2) + len(ctn3)

        ctn1._Container__prepend(ctn2)
        ctn1._Container__prepend(ctn3)
        self.assertEqual(len(ctn1), expected)

    def dunder_prepend_list_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, Context())
        models = [bases.Model({}), bases.Model({})]

        expected = len(ctn) + len(models)

        ctn._Container__prepend(models)
        self.assertEqual(len(ctn), expected)

    def dunder_prepend_item_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, Context())

        expected = len(ctn) + 1

        ctn._Container__prepend(bases.Model({}))
        self.assertEqual(len(ctn), expected)

    def dunder_previous_no_hal_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        ctn.hal = None
        self.assertFalse(ctn._Container__previous())

        ctn.hal = {}
        self.assertFalse(ctn._Container__previous())

    @mock.patch('amber_lib.client.send')
    @mock.patch('amber_lib.client.Container._Container__prepend')
    def dunder_previous_test(self, mock_prepend, mock_send):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        ctn.hal = {"previous": {"href": "http://example.com/previous"}}

        embedded = {"models": [0, 1, 2, 3]}
        hal_return = {"_embedded": embedded}

        mock_send.return_value = hal_return

        ctn._Container__previous()

        self.assertTrue(mock_send.called)
        mock_prepend.assert_called_with(embedded['models'])

    def append_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        model = bases.Model(Context())

        before = len(ctn)
        ctn.append(model)

        self.assertEqual(len(ctn), before + 1)
        self.assertEqual(ctn[-1], model)

    def count_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        self.assertEqual(ctn.count(), len(ctn))

    def extend_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        model = bases.Model(Context())

        before = len(ctn)
        ctn.extend(model)

        self.assertEqual(len(ctn), before + 1)
        self.assertEqual(ctn[-1], model)

    def index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        index = 1

        self.assertEqual(ctn.index(ctn[index]), index)

    def index_non_existant_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        self.assertRaises(ValueError, lambda: ctn.index("foobar"))



    def insert_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, Context())

        expected = len(ctn) + 1
        model = bases.Model({})
        second = ctn[1]

        ctn.insert(1, model)
        self.assertEqual(len(ctn), expected)
        self.assertEqual(ctn[1], model)
        self.assertEqual(ctn[2], second)

    def pop_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        length = len(ctn)

        ctn.pop()
        self.assertEqual(len(ctn), length - 1)

    def pop_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())
        length = len(ctn)

        model = ctn.pop(1)
        self.assertEqual(len(ctn), length - 1)

        for item in ctn:
            self.assertNotEqual(item, model)

        ctn[0]
        ctn[1]

        self.assertRaises(IndexError, lambda: ctn[2])



    def delete_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, Context())

        second = ctn[1]

        ctn.remove(second)

        self.assertEqual(len(ctn), 2)
        self.assertEqual(ctn[1]._links, "third")
        self.assertNotIn(second, ctn)

    def delete_invalid_index_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, Context())

        def delete_index():
            ctn.remove("foobar")
        self.assertRaises(ValueError, delete_index)

    def reverse_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, Context())
        reversed_ctn = reversed(ctn)
        ctn.reverse()

        self.assertEqual(reversed_ctn.values, ctn.values)
















if __name__ == "__main__":
    unittest.main()
