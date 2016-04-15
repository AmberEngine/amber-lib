#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys
import unittest

import mock

from amber_lib.models import bases
from amber_lib import client

FAKE_DATE = datetime(2015, 11, 30, 22, 36, 52, 538755)
FAKE_DATE_FORMAT = datetime.isoformat(FAKE_DATE)


class Context(object):
    public = 'mwyclv6bac2lqn9artt1o88laq4muk88483opkp9dnv8289f8olqrxlx7b2s7q8'
    private = "sn4ikxumkpi5dqb0vwo1ujbi68uv3bvoak1p0xzgbzhg71v9p1sn7a2t49dh2tz"
    host = "http://example.com"
    port = "8080"


class TestChild(bases.Model):
    _resource = "testchild"
    hey = bases.Property(str)


class TestInheritsModel(TestChild):
    _resource = "testinheritsmodel"
    listen = bases.Property(str)


class TestModel(bases.Model):
    _resource = "testmodels"
    id = bases.Property(int)
    foo = bases.Property(str)
    fizz = bases.Property(int, True)
    model = bases.Property(TestChild)
    testchild_list = bases.Property(TestChild, True)


class Model(unittest.TestCase):
    def test__init__(self):
        ctx = Context()

        model = bases.Model(ctx)
        self.assertEqual(model._ctx, ctx)

    def test__getattr__(self):
        known_attr = "_ctx"

        ctx = Context()
        model = bases.Model(ctx)

        self.assertEqual(getattr(model, known_attr), ctx)

    def test__getattr__missing_attribute(self):
        known_attr = "this_doesnt_exist"

        ctx = Context()
        model = bases.Model(ctx)

        self.assertRaises(AttributeError, getattr, *[model, known_attr])

    def test__getattr__(self):
        model = bases.Model(Context())
        with self.assertRaises(AttributeError):
            a = model.doesNotExist

    def test__getattribute__missing(self):
        model = TestModel(Context())
        self.assertRaises(AttributeError, model.__getattribute__, 'nope')

    def test__getattribute__private(self):
        ctx = Context()

        class TestModel2(TestModel):
            _test = None

        model = TestModel2(ctx)
        self.assertEqual(model.__getattribute__('_ctx'), ctx)
        self.assertEqual(model.__getattribute__('_test'), None)
        self.assertNotIn('_test', model.__dict__)

    def test__getattribute__callable(self):
        ctx = Context()

        def test(x):
            return 3

        class TestModel2(TestModel):
            my_func = test

        model = TestModel2(ctx)
        self.assertEqual(model.__getattribute__('my_func')(), 3)

    def dunder_getattribute_existing_property_test(self):
        ctx = Context()
        model = TestModel(ctx)

        prop = bases.Property(str)
        text = 'fubar'

        prop.__set__(prop, text)
        model.__dict__['foo'] = prop

        prop = model.__getattribute__('foo')

        self.assertEqual(prop, text)
        self.assertTrue(not isinstance(prop, bases.Property))

    def test__getattribute__public(self):
        model = bases.Model(Context())

        class Prop(object):
            value = "bar"

        model.__dict__["foo"] = Prop()

        self.assertEqual(model.__getattribute__("foo"), "bar")

    def test__getattribute__private(self):
        model = bases.Model(Context())
        model.__dict__["__foo__"] = "bar"

        self.assertEqual(model.__getattribute__("__foo__"),  "bar")

    def test__getattribute__invalid_private(self):
        model = bases.Model(Context())

        with self.assertRaises(AttributeError):
            model.__getattribute__("__na__")

    @mock.patch('amber_lib.models.bases.getattr')
    def dunder_setattr_known_attribute_test(self, mock_getattr):
        ctx1 = Context()
        ctx2 = Context()
        ctx2.port = "1337"

        model = bases.Model(ctx1)
        model._ctx = ctx2

        self.assertEqual(model._ctx, ctx2)

    @mock.patch('amber_lib.models.bases.getattr')
    def dunder_setattr_known_attribute_test(self, mock_getattr):
        ctx1 = Context()
        ctx2 = Context()
        ctx2.port = "1337"

        model = bases.Model(ctx1)

        def effect():
            raise AttributeError
        side_effect = effect

        self.assertRaises(
            AttributeError,
            setattr,
            *[model, "does_not_exist", ctx2]
        )

    @mock.patch('amber_lib.models.bases.getattr')
    def dunder_setattr_use_parent_attribute_test(self, mock_getattr):
        class Second(bases.Model):
            second = bases.Property(str)

        class Third(Second):
            third = bases.Property(str)

        class First(bases.Model):
            first = bases.Property(str)
            third = bases.Property(Third)

        f = First(Context())
        f.third = Third(Context())
        f.third.second = 'test'

        self.assertEqual(f.third.second, 'test')

    def test__setattr__private(self):
        model = bases.Model(Context())
        value = -42
        model._id = -42

        self.assertEqual(model.__dict__["_id"], value)

    def test__setattr__public(self):
        model = bases.Model(Context())

        class Prop(object):
            value = 0

            def __set__(self, object, value):
                self.value = value

        model.__dict__["foo"] = Prop()
        value = -42

        model.foo = value

        self.assertEqual(model.__dict__["foo"].value, value)

    @mock.patch('amber_lib.models.bases.find')
    def test__setattr__missing_class_attribute(self, mock_find):
        model = bases.Model(Context())
        mock_find.return_value = None
        with self.assertRaises(AttributeError):
            model.doesNotExist = "foobar"

    @mock.patch('amber_lib.models.bases.setattr')
    @mock.patch('amber_lib.models.bases.Property')
    @mock.patch('amber_lib.models.bases.find')
    def test__setattr__class_attribute(
        self,
        mock_find,
        mock_prop,
        mock_setattr
    ):
        model = bases.Model(Context())
        mock_find.return_value = mock.Mock()
        mock_find.return_value.kind = "int"
        mock_find.return_value.is_list = False

        model.thing = "fizzbuzz"
        mock_prop.assert_called_with("int", False)
        mock_setattr.assert_called_with(model, "thing", "fizzbuzz")

    def test_clear(self):
        model = bases.Model(Context())
        model.__dict__['_private'] = 'private_attr'
        model.__dict__['func'] = lambda x: x
        model.__dict__['public'] = 'foobar'

        curr_len = len(model.__dict__)
        public_count = 1

        model.clear()
        self.assertEqual(len(model.__dict__), curr_len - public_count)

    def test_ctx(self):
        ctx = Context()
        model = bases.Model(ctx)

        self.assertEqual(model.ctx(), ctx)

    @mock.patch('amber_lib.models.bases.Model.is_valid')
    def test_delete_valid_id_not_none(self, mock_is_valid):
        model = bases.Model(Context())
        mock_is_valid.return_value = True
        with self.assertRaises(ValueError):
            model.delete(0)

    @mock.patch('amber_lib.models.bases.client.send')
    @mock.patch('amber_lib.models.bases.Model.is_valid')
    def test_delete_valid_id_none(self, mock_is_valid, mock_send):
        ctx = Context()
        model = bases.Model(ctx)

        class Prop(object):
            value = 42

        model.__dict__['id'] = Prop()
        mock_is_valid.return_value = True

        result = model.delete()
        mock_send.assert_called_with('delete', ctx, '/models/42', None)
        self.assertDictEqual(result.__dict__, {})

    @mock.patch('amber_lib.models.bases.client.send')
    def test_delete_not_valid_id_passed(self, mock_send):
        ctx = Context()
        model = bases.Model(ctx)

        class Prop(object):
            value = 0

            def __set__(self, object, value):
                self.value = value

        model.__dict__['id'] = Prop()

        result = model.delete(42)
        mock_send.assert_called_with('delete', ctx, '/models/42', None)
        self.assertDictEqual(result.__dict__, {})

    @mock.patch('amber_lib.models.bases.client.send')
    @mock.patch('amber_lib.models.bases.Model.is_valid')
    def test_delete_not_valid_id_none(self, mock_is_valid, mock_send):
        ctx = Context()
        model = bases.Model(ctx)

        class Prop(object):
            value = 0

            def __set__(self, object, value):
                self.value = value

        model.__dict__['id'] = Prop()
        mock_is_valid.return_value = False

        with self.assertRaises(ValueError):
            model.delete()

    @mock.patch('amber_lib.models.bases.Model.pk')
    @mock.patch('amber_lib.models.bases.Model.is_valid')
    def test_endpoint_valid_zero_pk(self, mock_is_valid, mock_pk):
        model = bases.Model(Context())
        mock_is_valid.return_value = True
        mock_pk.return_value = 0
        with self.assertRaises(TypeError):
            model.endpoint()

    @mock.patch('amber_lib.models.bases.Model.pk')
    @mock.patch('amber_lib.models.bases.Model.is_valid')
    def test_endpoint_invalid_zero_pk(self, mock_is_valid, mock_pk):
        model = bases.Model(Context())
        mock_is_valid.return_value = False
        mock_pk.return_value = 0
        self.assertEqual(model.endpoint(), '/models')

    @mock.patch('amber_lib.models.bases.Model.pk')
    @mock.patch('amber_lib.models.bases.Model.is_valid')
    def test_endpoint_valid_non_zero_id(self, mock_is_valid, mock_pk):
        model = bases.Model(Context())
        mock_is_valid.return_value = True
        mock_pk.return_value = 42
        self.assertEqual(model.endpoint(), '/models/42')

    @mock.patch('amber_lib.models.bases.client.send')
    def test_form_schema(self, mock_send):
        model = bases.Model(Context())
        model._resource = 'model'
        url = "/form_schemas/%s" % model._resource

        model.form_schema()
        mock_send.assert_called_with(client.GET, model.ctx(), url, {})

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

    def test_is_valid(self):
        model = bases.Model(Context())

        class Prop(object):
            value = 0

        p = Prop()
        p.value = 0
        model.__dict__['id'] = p
        self.assertEqual(model.is_valid(), False)

        p.value = 'bar'
        model.__dict__['id'] = p
        self.assertEqual(model.is_valid(), False)

        p.value = '42'
        model.__dict__['id'] = p
        self.assertEqual(model.is_valid(), True)

        p.value = 42
        model.__dict__['id'] = p
        self.assertEqual(model.is_valid(), True)

    def test_pk(self):
        model = bases.Model(Context())

        class Prop(object):
            value = 42

        model.__dict__['id'] = Prop()
        self.assertEqual(model.pk(), 42)

    @mock.patch('amber_lib.models.bases.client.Container')
    @mock.patch('amber_lib.models.bases.Model.endpoint')
    @mock.patch('amber_lib.models.bases.client.send')
    def query_test(self, mock_send, mock_endpoint, mock_container):
        model = bases.Model(Context())

        model.query()

        self.assertTrue(mock_send.called)
        self.assertTrue(mock_endpoint.called)
        self.assertTrue(mock_container.called)

    @mock.patch('amber_lib.models.bases.Model.refresh')
    @mock.patch('amber_lib.models.bases.Model.pk')
    @mock.patch('amber_lib.client.send')
    @mock.patch('amber_lib.models.bases.Model.save')
    def test_set_relation(self, mock_save, mock_send, mock_pk, mock_refresh):
        model = bases.Model(Context())
        obj = mock.Mock()
        obj._resource = "res"
        obj.pk = mock.Mock()

        model.set_relation(True, obj)
        mock_save.assert_called_with()
        mock_send.assert_called_with(
            client.POST,
            model.ctx(),
            "/relations",
            **{
                model._resource: mock_pk(),
                obj._resource: obj.pk()
            }
        )
        mock_refresh.assert_called_with()

    @mock.patch('amber_lib.models.bases.Model.set_relation')
    def test_relate(self, mock_relation):
        model = bases.Model(Context())
        obj = mock.Mock()
        model.relate(obj)

        mock_relation.assert_called_with(True, obj)

    @mock.patch('amber_lib.models.bases.Model.from_dict')
    @mock.patch('amber_lib.models.bases.Model.endpoint')
    @mock.patch('amber_lib.models.bases.Model.ctx')
    @mock.patch('amber_lib.client.send')
    def retrieve_test(
            self,
            mock_send,
            mock_ctx,
            mock_endpoint,
            mock_from_dict
    ):
        model = TestModel(Context())
        model.id = 5
        model.retrieve(model.id)

        self.assertTrue(mock_send.called)
        self.assertTrue(mock_endpoint.called)
        self.assertTrue(mock_from_dict.called)
        self.assertTrue(mock_ctx.called)

    @mock.patch('amber_lib.models.bases.Model.pk')
    @mock.patch('amber_lib.models.bases.Model.retrieve')
    @mock.patch('amber_lib.models.bases.Model.is_valid')
    def test_refresh_invalid_object(
        self,
        mock_validity,
        mock_retrieve,
        mock_pk
    ):
        model = bases.Model(Context())
        mock_validity.return_value = False

        with self.assertRaises(Exception):
            model.refresh()
        mock_validity.assert_called_with()

    @mock.patch('amber_lib.models.bases.Model.pk')
    @mock.patch('amber_lib.models.bases.Model.retrieve')
    @mock.patch('amber_lib.models.bases.Model.is_valid')
    def test_refresh_valid_object(self, mock_validity, mock_retrieve, mock_pk):
        model = bases.Model(Context())
        mock_validity.return_value = True

        model.refresh()
        mock_validity.assert_called_with()
        mock_retrieve.assert_called_with(mock_pk())

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

    @mock.patch('amber_lib.models.bases.Model.set_relation')
    def test_unrelate(self, mock_relation):
        model = bases.Model(Context())
        obj = mock.Mock()
        model.unrelate(obj)

        mock_relation.assert_called_with(False, obj)

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


class Property(unittest.TestCase):
    def dunder_init_test(self):
        kind = str
        is_list = False

        prop = bases.Property(kind, is_list)
        self.assertEqual(prop.kind, kind)
        self.assertEqual(prop.is_list, is_list)
        self.assertEqual(prop.value, None)

    def dunder_set_none_test(self):
        class TestProp(object):
            prop = bases.Property(str)

        test = TestProp()
        test.prop = 'test'
        self.assertEqual(test.prop.value, 'test')

        test.prop = None
        self.assertEqual(test.prop.value, None)

    def dunder_set_list_not_list_test(self):
        class TestProp(object):
            prop = bases.Property(str, True)

        test = TestProp()

        def set_it():
            test.prop = 'not_a_list'

        self.assertRaises(TypeError, set_it)
        self.assertEqual(test.prop.value, [])

    def dunder_set_list_invalid_element_type_test(self):
        class TestProp(object):
            prop = bases.Property(int, True)

        test = TestProp()

        def set_it():
            test.prop = ['a', 'b', 'c']

        self.assertRaises(TypeError, set_it)
        self.assertEqual(test.prop.value, [])

    def dunder_set_list_valid_element_type_test(self):
        class TestProp(object):
            prop = bases.Property(str, True)

        test = TestProp()

        list_ = ['one', 'two', 'three', 'four']
        test.prop = list_

        self.assertEqual(test.prop.value, list_)

    def dunder_set_valid_type_test(self):
        class TestProp(object):
            prop = bases.Property(int)

        test = TestProp()

        magic_number = 43
        test.prop = magic_number

        self.assertEqual(test.prop.value, magic_number)

    def dunder_set_unicode_type_for_str_test(self):
        class TestProp(object):
            prop = bases.Property(str)

        test = TestProp()

        magic_str = u'Klüft skräms inför på fédéral électoral große'
        test.prop = magic_str

        self.assertTrue(isinstance(test.prop.value, str))

        if sys.version_info.major < 3:
            self.assertEqual(test.prop.value, magic_str.encode('utf-8'))
        else:
            self.assertEqual(test.prop.value, magic_str)

    def dunder_set_convert_int_for_float_test(self):
        class testprop(object):
            prop = bases.Property(float)

        test = testprop()

        killed_mobs = 42
        test.prop = killed_mobs

        self.assertTrue(isinstance(test.prop.value, float))
        self.assertEqual(test.prop.value, killed_mobs)

    def dunder_set_invalid_type(self):
        class testprop(object):
            prop = bases.Property(bool)

        test = testprop()

        def set_it():
            test.prop = 'i am not a bool'

        self.assertRaises(TypeError, set_it)


if __name__ == "__main__":
    unittest.main()
