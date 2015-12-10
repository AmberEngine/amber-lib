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
    testchild_list = bases.Property(TestChild, True)

FAKE_DATE = datetime(2015, 11, 30, 22, 36, 52, 538755)
FAKE_DATE_FORMAT = datetime.isoformat(FAKE_DATE)


class Model(unittest.TestCase):
    def init_test(self):
        ctx = Context()

        model = bases.Model(ctx)
        self.assertEqual(model._ctx, ctx)

    def ctx_test(self):
        ctx = Context()
        model = bases.Model(ctx)

        self.assertEqual(model.ctx(), ctx)

    def dunder_getattribute_missing_test(self):
        model = TestModel(Context())
        self.assertRaises(AttributeError, model.__getattribute__, 'nope')

    def dunder_getattribute_underscored_test(self):
        ctx = Context()
        class TestModel2(TestModel):
            _test = None

        model = TestModel2(ctx)
        self.assertEqual(model.__getattribute__('_ctx'), ctx)
        self.assertEqual(model.__getattribute__('_test'), None)
        self.assertNotIn('_test', model.__dict__)

    def dunder_getattribute_callable_test(self):
        ctx = Context()
        class TestModel2(TestModel):
            my_func = lambda x: 3

        model = TestModel2(ctx)
        self.assertEqual(model.__getattribute__('my_func')(), 3)


    def dunder_getattribute_new_property_test(self):
        ctx = Context()
        model = TestModel(ctx)

        self.assertNotIn('foo', model.__dict__)

        prop = model.__getattribute__('foo')

        self.assertTrue(isinstance(prop, bases.Property))
        self.assertIn('foo', model.__dict__)


    def dunder_getattribute_existing_property_test(self):
        ctx = Context()
        model = TestModel(ctx)

        text = 'fubar'
        model.__dict__['foo'] = text

        prop = model.__getattribute__('foo')

        self.assertEqual(prop, text)
        self.assertTrue(not isinstance(prop, bases.Property))

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
        model.id.value = "foobar_2"

        self.assertRaises(TypeError, model.endpoint)

    def from_dict_test(self):
        dict_ = {
            'foo': 'bar',
            'fizz': [1, 2, 3],
            'model': {
                'hey': 'Listen!'
            },
            'testchild_list': [
                {'hey': 'Listen to me!'},
                {'hey': 'Listen two me!'}
            ]
        }

        model = TestModel(Context())
        model.from_dict(dict_)

        self.assertEqual(model.foo, 'bar')
        self.assertEqual(model.fizz, [1, 2, 3])
        self.assertEqual(model.model.hey, 'Listen!')
        self.assertEqual(len(model.testchild_list), 2)

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
    def from_json_test(self, mock_from_dict):
        json = '{"foo": "bar", "fizz": [1, 2, 3]}'
        model = bases.Model(Context())

        model.from_json(json)
        self.assertTrue(mock_from_dict.called)


    @mock.patch('amber_lib.models.bases.Model.update')
    @mock.patch('amber_lib.models.bases.Model.ctx')
    @mock.patch('amber_lib.models.bases.Model.endpoint')
    @mock.patch('amber_lib.models.bases.Model.to_dict')
    @mock.patch('amber_lib.client.send')
    def save_update_test(
        self,
        mock_send,
        mock_dict,
        mock_end,
        mock_ctx,
        mock_update
    ):
        model = TestModel(Context())
        model.id = 49
        model.save()

        self.assertEqual(mock_update.call_count, 1)

        self.assertTrue(mock_send.called)
        self.assertTrue(mock_dict.called)
        self.assertTrue(mock_end.called)
        self.assertTrue(mock_ctx.called)
        self.assertTrue(mock_send.called)

        mock_send.assert_called_with(
            'put',
            mock_ctx(),
            mock_end(),
            mock_dict()
        )

    @mock.patch('amber_lib.models.bases.Model.update')
    @mock.patch('amber_lib.models.bases.Model.ctx')
    @mock.patch('amber_lib.models.bases.Model.endpoint')
    @mock.patch('amber_lib.models.bases.Model.to_dict')
    @mock.patch('amber_lib.client.send')
    def save_create_test(
        self,
        mock_send,
        mock_dict,
        mock_end,
        mock_ctx,
        mock_update
    ):
        model = TestModel(Context())


        model.save('{"foo": "bar"}')

        self.assertEqual(mock_update.call_count, 2)

        self.assertTrue(mock_send.called)
        self.assertTrue(mock_dict.called)
        self.assertTrue(mock_end.called)
        self.assertTrue(mock_ctx.called)
        self.assertTrue(mock_send.called)

        mock_send.assert_called_with(
            'post',
            mock_ctx(),
            mock_end(),
            mock_dict()
        )


    def to_dict_test(self):
        model = TestModel(Context())

        model.foo = 'bar'
        model.fizz = [1, 2, 3]
        model.testchild_list = [TestChild(Context())]
        model.model = TestChild(Context())
        model.model.hey = 'Listen!'

        dict_ = model.to_dict()

        self.assertIn('foo', dict_)
        self.assertIn('fizz', dict_)
        self.assertIn('model', dict_)
        self.assertIn('id', dict_)
        self.assertIn('hey', dict_['model'])

    @mock.patch('amber_lib.models.bases.Model.to_dict')
    @mock.patch('amber_lib.models.bases.json.dumps')
    def to_json_test(self, mock_dumps, mock_to_dict):
        model = TestModel(Context())

        model.to_json()
        self.assertTrue(mock_dumps.called)
        self.assertTrue(mock_to_dict.called)

    @mock.patch('amber_lib.models.bases.Model.from_dict')
    def update_dict_test(self, mock_dict):
        model = TestModel(Context())
        model.update({})

        self.assertTrue(mock_dict.called)

    @mock.patch('amber_lib.models.bases.Model.from_json')
    def update_json_test(self, mock_json):
        model = TestModel(Context())
        model.update('{}')

        self.assertTrue(mock_json.called)

    def update_invalid_arg_type_test(self):
        model = TestModel(Context())
        self.assertRaises(TypeError, lambda: model.update(3.14159))

    @mock.patch('amber_lib.models.bases.Model.from_dict')
    @mock.patch('amber_lib.models.bases.Model.endpoint')
    @mock.patch('amber_lib.models.bases.Model.ctx')
    @mock.patch('amber_lib.client.send')
    def retrieve_test(self, mock_send, mock_ctx, mock_endpoint, mock_from_dict):
        model = TestModel(Context())
        print("&"*100)
        model.id = 5
        print(model.id)
        model.retrieve(model.id)
        print("#"*100)

        self.assertTrue(mock_send.called)
        self.assertTrue(mock_endpoint.called)
        self.assertTrue(mock_from_dict.called)
        self.assertTrue(mock_ctx.called)


if __name__ == "__main__":
    unittest.main()
