#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import unittest
import sys

import mock

from . import components


class Context(object):
    public = 'mwyclv6bac2lqn9artt1o88laq4muk88483opkp9dnv8289f8olqrxlx7b2s7q8'
    private = "sn4ikxumkpi5dqb0vwo1ujbi68uv3bvoak1p0xzgbzhg71v9p1sn7a2t49dh2tz"
    host = "http://example.com"
    port = "8080"


class TestChild(components.Model):
    _resource = "testchild"
    hey = components.Property(str)


class TestInheritsModel(TestChild):
    _resource = "testinheritsmodel"
    listen = components.Property(str)


class TestModel(components.Model):
    _resource = "testmodels"
    id = components.Property(int)
    foo = components.Property(str)
    fizz = components.Property(int, True)
    model = components.Property(TestChild)
    testchild_list = components.Property(TestChild, True)

FAKE_DATE = datetime(2015, 11, 30, 22, 36, 52, 538755)
FAKE_DATE_FORMAT = datetime.isoformat(FAKE_DATE)


class Component(unittest.TestCase):
    @mock.patch('amber_lib.models.components.Component.endpoint')
    @mock.patch('amber_lib.models.components.Component.ctx')
    @mock.patch('amber_lib.client.send')
    @mock.patch('amber_lib.models.components.Component.is_valid')
    def delete_valid_entry_test(
            self,
            mock_is_valid,
            mock_send,
            mock_ctx,
            mock_endpoint
        ):
        model = components.Component(Context())
        model.component_data_id = 5

        mock_is_valid.return_value = True

        model.delete(model.component_data_id)

        self.assertTrue(mock_send.called)
        self.assertTrue(mock_endpoint.called)
        self.assertTrue(mock_ctx.called)

    @mock.patch('amber_lib.models.components.Component.endpoint')
    @mock.patch('amber_lib.models.components.Component.ctx')
    @mock.patch('amber_lib.client.send')
    @mock.patch('amber_lib.models.components.Component.is_valid')
    def delete_invalid_entry_test(
            self,
            mock_is_valid,
            mock_send,
            mock_ctx,
            mock_endpoint
        ):
        model = components.Component(Context())
        model.component_data_id = 5

        mock_is_valid.return_value = False

        self.assertRaises(ValueError, lambda: model.delete())

    def endpoint_no_id_test(self):
        model = components.Component(Context())
        self.assertEqual(model.endpoint(), '/components/component')

    def endpoint_int_id_test(self):
        model = components.Component(Context())
        model.component_data_id = 1

        print(type(getattr(model, model._pk)))
        self.assertEqual(model.endpoint(), '/components/component/1')

    @mock.patch('amber_lib.models.components.Component.from_dict')
    @mock.patch('amber_lib.models.components.Component.endpoint')
    @mock.patch('amber_lib.models.components.Component.ctx')
    @mock.patch('amber_lib.client.send')
    def retrieve_test(
            self,
            mock_send,
            mock_ctx,
            mock_endpoint,
            mock_from_dict
        ):
        model = components.Component(Context())
        model.component_data_id = 5
        model.retrieve(model.component_data_id)

        self.assertTrue(mock_send.called)
        self.assertTrue(mock_endpoint.called)
        self.assertTrue(mock_from_dict.called)
        self.assertTrue(mock_ctx.called)

    @mock.patch('amber_lib.models.components.Component.update')
    @mock.patch('amber_lib.models.components.Component.ctx')
    @mock.patch('amber_lib.models.components.Component.endpoint')
    @mock.patch('amber_lib.models.components.Component.to_dict')
    @mock.patch('amber_lib.client.send')
    def save_update_test(
        self,
        mock_send,
        mock_dict,
        mock_end,
        mock_ctx,
        mock_update
    ):
        model = components.Component(Context())
        model.component_data_id = 49
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

    @mock.patch('amber_lib.models.components.Component.update')
    @mock.patch('amber_lib.models.components.Component.ctx')
    @mock.patch('amber_lib.models.components.Component.endpoint')
    @mock.patch('amber_lib.models.components.Component.to_dict')
    @mock.patch('amber_lib.client.send')
    def save_create_test(
        self,
        mock_send,
        mock_dict,
        mock_end,
        mock_ctx,
        mock_update
    ):
        model = components.Component(Context())


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
