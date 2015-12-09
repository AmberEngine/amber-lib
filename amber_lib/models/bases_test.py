from datetime import datetime
import os
import unittest
import sys

import mock

from . import bases


class Context(object):
    public = 'mwyclv6bac2lqn9artt1o88laq4muk88483opkp9dnv8289f8olqrxlx7b2s7q8'
    private = "sn4ikxumkpi5dqb0vwo1ujbi68uv3bvoak1p0xzgbzhg71v9p1sn7a2t49dh2tz"
    host = "http://example.com"
    port = "8080"


class TestChild(bases.Model):
    hey = bases.Property(str)


class TestModel(bases.Model):
    id = bases.Property(int)
    foo = bases.Property(str)
    fizz = bases.Property(int, True)
    model = bases.Property(TestChild)


FAKE_DATE = datetime(2015, 11, 30, 22, 36, 52, 538755)
FAKE_DATE_FORMAT = datetime.isoformat(FAKE_DATE)


class Model(unittest.TestCase):
    def setUp(self):
        bases.Model.id = None

    def init_test(self):
        ctx = Context()

        model = bases.Model(ctx)
        self.assertEqual(model._ctx, ctx)

    def get_known_attribute_test(self):
        known_attr = "_ctx"

        ctx = Context()
        model = bases.Model(ctx)

        self.assertEqual(getattr(model, known_attr), ctx)

    def get_unknown_attribute_test(self):
        known_attr = "this_doesnt_exist"

        ctx = Context()
        model = bases.Model(ctx)

        self.assertRaises(AttributeError, getattr, *[model, known_attr])

    @mock.patch('amber_lib.models.bases.getattr')
    def set_known_attribute_test(self, mock_getattr):
        ctx1 = Context()
        ctx2 = Context()
        ctx2.port = "1337"

        model = bases.Model(ctx1)
        model._ctx = ctx2

        self.assertEqual(model._ctx, ctx2)

    @mock.patch('amber_lib.models.bases.getattr')
    def set_known_attribute_test(self, mock_getattr):
        ctx1 = Context()
        ctx2 = Context()
        ctx2.port = "1337"

        model = bases.Model(ctx1)

        side_effect = lambda _, __: (_ for _ in ()).throw(AttributeError(''))
        mock_getattr.side_effect = side_effect

        self.assertRaises(
            AttributeError,
            setattr,
            *[model, "does_not_exist", ctx2]
        )

    @mock.patch('amber_lib.models.bases.client.Container')
    @mock.patch('amber_lib.models.bases.Model.endpoint')
    @mock.patch('amber_lib.models.bases.client.send')
    def query_test(self, mock_send, mock_endpoint, mock_container):
        model = bases.Model(Context())

        model.query()

        self.assertTrue(mock_send.called)
        self.assertTrue(mock_endpoint.called)
        self.assertTrue(mock_container.called)

    def endpoint_no_id_test(self):
        model = bases.Model(Context())
        self.assertEqual(model.endpoint(), '/models')

    def endpoint_int_id_test(self):
        model = TestModel(Context())
        model.id = 1

        self.assertEqual(model.endpoint(), '/testmodels/1')

    def endpoint_int_property_test(self):
        model = TestModel(Context())
        model.id.set(5)

        self.assertEqual(model.endpoint(), '/testmodels/5')

    def endpoint_wrong_id_type_test(self):
        model = TestModel(Context())
        model.id.value = "foobar"

        self.assertRaises(TypeError, model.endpoint)

    def from_dict_test(self):
        dict_ = {
            'foo': 'bar',
            'fizz': [1, 2, 3],
            'model': {
                'hey': 'Listen!'
            }
        }

        model = TestModel(Context())
        model.from_dict(dict_)

        self.assertEqual(model.foo, 'bar')
        self.assertEqual(model.fizz, [1, 2, 3])
        self.assertEqual(model.model.hey, 'Listen!')

    def from_dict_bad_data_test(self):
        dict_ = {
            'foo': 'bar',
            'fizz': [1, 2, 3],
            'model': {
                'hey': 'Listen!'
            },
            'i_dont_exist': 'NOPE!'
        }

        model = TestModel(Context())

        self.assertRaises(AttributeError, model.from_dict, dict_)

    @mock.patch('amber_lib.models.bases.Model.from_dict')
    def from_json(self, mock_from_dict):
        json = '{"foo": "bar", "fizz": [1, 2, 3]}'
        model = bases.Model(Contect())

        model.from_json(json)
        self.assertTrue(mock_from_dict.called)



if __name__ == "__main__":
    unittest.main()
