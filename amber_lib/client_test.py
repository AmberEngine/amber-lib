from datetime import datetime
import math
import os
import unittest
import sys

import mock

from amber_lib import client
from amber_lib.models import bases


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


class TestContext(object):
    public = 'mwyclv6bac2lqn9artt1o88laq4muk88483opkp9dnv8289f8olqrxlx7b2s7q8'
    private = "sn4ikxumkpi5dqb0vwo1ujbi68uv3bvoak1p0xzgbzhg71v9p1sn7a2t49dh2tz"
    host = "http://example.com"
    port = "8080"
    request_attempts = 3

class Context(unittest.TestCase):
    def dunder_init_valid_keys_test(self):
        args = {
            'host': 'http://amberlib.example.com',
            'port': '1337'
        }

        ctx = client.Context(**args)
        self.assertEqual(ctx.host, args['host'])
        self.assertEqual(ctx.port, args['port'])

    def dunder_init_invalid_keys_test(self):
        args = {
            'host': 'http://amberlib.example.com',
            'port': '1337',
            'fizz': 'buzz'
        }

        ctx = client.Context(**args)
        self.assertEqual(ctx.host, args['host'])
        self.assertEqual(ctx.port, args['port'])

        self.assertNotIn('fizz', ctx.__dict__)


class Container(unittest.TestCase):
    def all_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        self.assertEqual(ctn[:].values, ctn._Container__all().values)

    def append_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        model = bases.Model(TestContext())

        before = len(ctn)
        ctn.append(model)

        self.assertEqual(len(ctn), before + 1)
        self.assertEqual(ctn[-1], model)

    def count_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        self.assertEqual(ctn.count(), len(ctn))

    def delete_invalid_index_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, TestContext())

        def delete_index():
            ctn.remove("foobar")
        self.assertRaises(ValueError, delete_index)

    def delete_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        second = ctn[1]

        ctn.remove(second)

        self.assertEqual(len(ctn), 2)
        self.assertEqual(ctn[1]._links, "third")
        self.assertNotIn(second, ctn)

    def dunder_add_test(self):
        hal = {
            "_embedded": {
                "models": [
                    {"_links": "third"},
                ]
            },
            "_links": {},
            "total": 1
        }

        ctn1 = client.Container(FAKE_HAL, bases.Model, TestContext())
        ctn2 = client.Container(hal, bases.Model, TestContext())

        ctn3 = ctn1 + ctn2

        self.assertEqual(len(ctn1.values), 2)
        self.assertEqual(len(ctn2.values), 1)

        self.assertEqual(len(ctn3.values), 3)
        self.assertEqual(ctn3[-1]._links, "third")

    def dunder_add_wrong_type_test(self):
        ctn1 = client.Container(FAKE_HAL, bases.Model, TestContext())
        self.assertRaises(TypeError, lambda: ctn1 + "foobar")

    def dunder_append_container_test(self):
        ctn1 = client.Container(FAKE_HAL, bases.Model, TestContext())
        ctn2 = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        ctn3 = client.Container({}, bases.Model, TestContext())

        expected = len(ctn1) + len(ctn2) + len(ctn3)

        ctn1._Container__append(ctn2)
        ctn1._Container__append(ctn3)
        self.assertEqual(len(ctn1), expected)

    def dunder_append_item_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, TestContext())

        expected = len(ctn) + 1

        ctn._Container__append(bases.Model({}))
        self.assertEqual(len(ctn), expected)

    def dunder_append_list_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, TestContext())
        models = [bases.Model({}), bases.Model({})]

        expected = len(ctn) + len(models)

        ctn._Container__append(models)
        self.assertEqual(len(ctn), expected)

    def dunder_contains_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, TestContext())
        model = ctn[0]
        self.assertIn(model, ctn)
        self.assertNotIn("foobar", ctn)

    def dunder_delitem_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        second = ctn[1]

        del ctn[1]

        self.assertEqual(len(ctn), 2)
        self.assertEqual(ctn[1]._links, "third")
        self.assertNotIn(second, ctn)

    def dunder_delitem_invalid_index_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, TestContext())

        def delete_index():
            del ctn[100]
        self.assertRaises(IndexError, delete_index)

    @mock.patch('amber_lib.client.Container._Container__all')
    def dunder_finish_it_ignored_test(self, mock_all):
        ctn = client.Container(FAKE_HAL, bases.Model, TestContext())
        ctn._Container__finish_it()

        mock_all.assert_not_called()

    @mock.patch('amber_lib.client.Container._Container__all')
    def dunder_finish_it_test(self, mock_all):
        ctn = client.Container(FAKE_HAL, bases.Model, TestContext())
        ctn.total = 500
        ctn._Container__finish_it()

        mock_all.assert_called_with()

    def dunder_get_invalid_negative_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        too_far_under = len(ctn) * -1
        self.assertRaises(
            IndexError,
            lambda: ctn._Container__get(too_far_under)
        )

    def dunder_get_invalid_positive_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        self.assertRaises(IndexError, lambda: ctn._Container__get(len(ctn)))

    def dunder_get_positive_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        self.assertEqual(ctn._Container__get(0)._links, "first")

    @mock.patch('amber_lib.client.Container._Container__next')
    def dunder_get_use_next_test(self, mock_next):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

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
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        mock_previous.return_value = False

        del ctn.values[0]
        ctn.offset = 2
        ctn.total = 5

        def prev_values():
            ctn.values[0] = "first index"
            ctn.values[1] = "second"
            ctn.offset = 0

        mock_previous.side_effect = prev_values

        self.assertEqual(ctn._Container__get(0), "first index")
        mock_previous.assert_called_with()

    def dunder_get_valid_negative_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        model = ctn[2]

        self.assertEqual(ctn._Container__get(-1), model)

    def dunder_getitem_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        self.assertEqual(ctn[0]._links, "first")
        self.assertEqual(ctn[1]._links, "second")
        self.assertEqual(ctn[-1]._links, "third")

    def dunder_getitem_invalid_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        self.assertRaises(IndexError, lambda: ctn[42])
        self.assertRaises(IndexError, lambda: ctn[-99])

    def dunder_getitem_invalid_index_type_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        self.assertRaises(TypeError, lambda: ctn["one"])
        self.assertRaises(TypeError, lambda: ctn[3.14159])

    def dunder_getitem_invalid_slice_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        self.assertEqual(len(ctn[1:500]), 2)
        self.assertEqual(len(ctn[100:1001]), 0)

    def dunder_getitem_slice_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        self.assertEqual(len(ctn[:]), 3)
        self.assertEqual(len(ctn[0:2]), 2)
        self.assertEqual(len(ctn[0:3:2]), 2)

        self.assertEqual(ctn[0:2][1]._links, "second")

    def dunder_iter_no_items_test(self):
        ctn = client.Container({}, bases.Model, TestContext())
        count = 0

        for item in ctn:
            count += 1

        self.assertEqual(count, 0)

    def dunder_iter_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        values = ctn.values
        count = 0

        for item in ctn:
            self.assertEqual(values[count], item)
            count += 1

        self.assertEqual(count, len(ctn))

    def dunder_next_no_hal_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        ctn.hal = None
        self.assertFalse(ctn._Container__next())

        ctn.hal = {}
        self.assertFalse(ctn._Container__next())

    @mock.patch('amber_lib.client.send')
    @mock.patch('amber_lib.client.Container._Container__append')
    def dunder_next_test(self, mock_append, mock_send):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        ctn.hal = {"next": {"href": "http://example.com/next"}}

        embedded = {"models": [0, 1, 2, 3]}
        hal_return = {"_embedded": embedded}

        mock_send.return_value = hal_return

        ctn._Container__next()

        self.assertTrue(mock_send.called)
        mock_append.assert_called_with(embedded['models'])

    def dunder_prepend_container_test(self):
        ctn1 = client.Container(FAKE_HAL, bases.Model, TestContext())
        ctn2 = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        ctn3 = client.Container({}, bases.Model, TestContext())

        expected = len(ctn1) + len(ctn2) + len(ctn3)

        ctn1._Container__prepend(ctn2)
        ctn1._Container__prepend(ctn3)
        self.assertEqual(len(ctn1), expected)

    def dunder_prepend_list_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, TestContext())
        models = [bases.Model({}), bases.Model({})]

        expected = len(ctn) + len(models)

        ctn._Container__prepend(models)
        self.assertEqual(len(ctn), expected)

    def dunder_prepend_item_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, TestContext())

        expected = len(ctn) + 1

        ctn._Container__prepend(bases.Model({}))
        self.assertEqual(len(ctn), expected)

    def dunder_previous_no_hal_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        ctn.hal = None
        self.assertFalse(ctn._Container__previous())

        ctn.hal = {}
        self.assertFalse(ctn._Container__previous())

    @mock.patch('amber_lib.client.send')
    @mock.patch('amber_lib.client.Container._Container__prepend')
    def dunder_previous_test(self, mock_prepend, mock_send):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        ctn.hal = {"previous": {"href": "http://example.com/previous"}}

        embedded = {"models": [0, 1, 2, 3]}
        hal_return = {"_embedded": embedded}

        mock_send.return_value = hal_return

        ctn._Container__previous()

        self.assertTrue(mock_send.called)
        mock_prepend.assert_called_with(embedded['models'])

    def dunder_setitem_invalid_range_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        new_model = bases.Model({})
        new_model._links = "fourth"

        def temp():
            ctn[42] = new_model
        self.assertRaises(IndexError, temp)

    def dunder_setitem_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        new_model = bases.Model({})
        new_model._links = "fourth"

        ctn[2] = new_model

        self.assertEqual(len(ctn), 3)
        self.assertEqual(ctn[-1]._links, "fourth")

    def extend_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        model = bases.Model(TestContext())

        before = len(ctn)
        ctn.extend(model)

        self.assertEqual(len(ctn), before + 1)
        self.assertEqual(ctn[-1], model)

    def index_non_existant_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())

        self.assertRaises(ValueError, lambda: ctn.index("foobar"))

    def index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        index = 1

        self.assertEqual(ctn.index(ctn[index]), index)

    def insert_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, TestContext())

        expected = len(ctn) + 1
        model = bases.Model({})
        second = ctn[1]

        ctn.insert(1, model)
        self.assertEqual(len(ctn), expected)
        self.assertEqual(ctn[1], model)
        self.assertEqual(ctn[2], second)

    def le_api_test(self):
        ctn = client.Container({}, bases.Model, TestContext())
        self.assertTrue((ctn <= ctn).startswith("le"))

    def len_empty_test(self):
        ctn = client.Container({}, bases.Model, TestContext())
        self.assertEqual(len(ctn), 0)

    def len_total_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        self.assertEqual(len(ctn), 3)

    def len_values_test(self):
        ctn = client.Container({}, bases.Model, TestContext())

        class Length:
            def __len__(self):
                return 42

        ctn.values = Length()
        self.assertEqual(len(ctn), 42)

    def pop_index_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        length = len(ctn)

        model = ctn.pop(1)
        self.assertEqual(len(ctn), length - 1)

        for item in ctn:
            self.assertNotEqual(item, model)

        ctn[0]
        ctn[1]

        self.assertRaises(IndexError, lambda: ctn[2])

    def pop_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        length = len(ctn)

        ctn.pop()
        self.assertEqual(len(ctn), length - 1)

    def pow_test(self):
        ctn = client.Container({}, bases.Model, TestContext())
        self.assertTrue('Mario' in ctn ** 42)

    def reverse_test(self):
        ctn = client.Container(FAKE_HAL, bases.Model, TestContext())
        reversed_ctn = reversed(ctn)
        ctn.reverse()

        self.assertEqual(reversed_ctn.values, ctn.values)

    def reversed_test(self):
        ctn = client.Container(FAKE_HAL_THREE, bases.Model, TestContext())
        values = ctn[:]

        reversed_ctn = reversed(ctn)
        for i in range(len(reversed_ctn)):
            self.assertEqual(reversed_ctn[i], values[len(values) - i - 1])

    @mock.patch('amber_lib.client.send')
    def set_relation_relate_test(self, mock_send):
        type_ = "GET"
        tupperwear = client.Container({}, mock.Mock, {}, None)
        m = mock.Mock()
        m.id = 5
        m._resource = 'fubars'
        tupperwear.append(m)

        tupperwear.set_relation(type_, m)
        self.assertTrue(mock_send.called)

    @mock.patch('amber_lib.client.send')
    def set_relation_with_container_test(self, mock_send):
        type_ = "GET"
        tupperwear = client.Container({}, mock.Mock, TestContext(), None)
        m = mock.Mock()
        m.id = 5
        m._resource = 'fubars'
        tupperwear.append(m)

        jar = client.Container({}, mock.Mock, {}, None)
        jar.append(m)

        tupperwear.set_relation(type_, jar)
        self.assertTrue(mock_send.called)

    @mock.patch('amber_lib.client.Container.set_relation')
    def relate_test(self, mock_relation):
        bag = client.Container({}, mock.Mock, TestContext(), None)
        obj = mock.Mock()
        bag.relate(obj)

        self.assertTrue(mock_relation.called_once_with(client.POST, obj))


    @mock.patch('amber_lib.client.Container.set_relation')
    def unrelate_test(self, mock_relation):
        bag = client.Container({}, mock.Mock, TestContext(), None)
        obj = mock.Mock()
        bag.unrelate(obj)

        self.assertTrue(mock_relation.called_once_with(client.DELETE, obj))



class CreatePayload(unittest.TestCase):
    def create_payload_test(self):
        ctx = TestContext()
        url = "http://example.com/test"
        data = {"foo": "bar", "fizz": "buzz"}

        payload = client.create_payload(ctx, url, data)

        self.assertTrue('signature' in payload)


class CreateURL(unittest.TestCase):
    def create_url_test(self):
        endpoint = "/products/42"

        self.assertEqual(
            client.create_url(TestContext(), endpoint),
            "http://example.com:8080%s" % endpoint
        )

    def create_url_with_uri_test(self):
        endpoint = "/products/24"

        self.assertEqual(
            client.create_url(TestContext(), endpoint, limit=50, offset=3),
            "http://example.com:8080%s?limit=50&offset=3" % endpoint
        )


class Send(unittest.TestCase):
    @mock.patch('amber_lib.client.requests')
    def send_200_request_test(self, mock_requests):
        method = client.GET
        endpoint = "/products/1337"
        json_data = {}

        r = mock.MagicMock(status_code=200)
        mock_requests.get.return_value = r

        client.send(method, TestContext(), endpoint, {})

        self.assertTrue(mock_requests.get.called)

    @mock.patch('amber_lib.client.requests')
    def send_200_request_no_json_test(self, mock_requests):
        method = client.GET
        endpoint = "/products/1337"
        json_data = {}

        r = mock.MagicMock(status_code=200)

        def raise_value_error():
            raise ValueError()
        r.json.side_effect = raise_value_error
        mock_requests.get.return_value = r

        self.assertEqual(client.send(method, TestContext(), endpoint, {}), {})

    @mock.patch('amber_lib.client.requests')
    def send_500_request_test(self, mock_requests):
        method = client.GET
        endpoint = "/products/1337"
        json_data = {}

        r = mock.Mock()
        r.status_code = 500
        mock_requests.get.return_value = r

        self.assertRaises(
            Exception,
            lambda: client.send(method, TestContext(), endpoint, {})
        )

    @mock.patch('amber_lib.client.requests')
    def send_404_request_test(self, mock_requests):
        method = client.GET
        endpoint = "/products/1337"
        json_data = {}

        r = mock.Mock()
        r.status_code = 404

        mock_requests.get.return_value = r

        self.assertRaises(
            Exception,
            lambda: client.send(method, TestContext(), endpoint, {})
        )

    @mock.patch('amber_lib.client.requests')
    def send_500_request_no_json_test(self, mock_requests):
        method = client.GET
        endpoint = "/products/1337"
        json_data = {}

        r = mock.Mock(status_code=500)
        def raise_value_error():
            raise ValueError()
        r.json.side_effect = raise_value_error
        mock_requests.get.return_value = r

        self.assertRaises(
            Exception,
            lambda: client.send(method, TestContext(), endpoint, {})
        )


    @mock.patch('amber_lib.client.requests')
    def send_invalid_request_test(self, mock_requests):
        method = 'leet_haxors'
        endpoint = "/products/1337"
        json_data = {}

        self.assertRaises(
            AttributeError,
            lambda: client.send(method, TestContext(), endpoint, {})
        )


if __name__ == "__main__":
    unittest.main()
