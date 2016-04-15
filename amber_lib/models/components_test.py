#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import unittest
import sys

import mock

from . import components
from amber_lib import client


class Context(object):
    public = 'mwyclv6bac2lqn9artt1o88laq4muk88483opkp9dnv8289f8olqrxlx7b2s7q8'
    private = "sn4ikxumkpi5dqb0vwo1ujbi68uv3bvoak1p0xzgbzhg71v9p1sn7a2t49dh2tz"
    host = "http://example.com"
    port = "8080"


CONTEXT = Context()


class Component(unittest.TestCase):
    @mock.patch('amber_lib.models.components.client.send')
    @mock.patch('amber_lib.models.components.Component.pk')
    @mock.patch('amber_lib.models.components.Component.is_valid')
    def test_delete_has_invalid_id_arg(
        self,
        mock_is_valid,
        mock_pk,
        mock_send
    ):
        comp = components.Component(CONTEXT)

        mock_is_valid.return_value = True
        mock_pk.return_value = 1
        arg_id = 321

        with self.assertRaises(ValueError):
            comp.delete(arg_id)
        mock_is_valid.assert_called_with()
        mock_pk.assert_called_with()

    @mock.patch('amber_lib.models.components.Component.clear')
    @mock.patch('amber_lib.models.components.client.send')
    @mock.patch('amber_lib.models.components.setattr')
    @mock.patch('amber_lib.models.components.Component.pk')
    @mock.patch('amber_lib.models.components.Component.is_valid')
    def test_delete_has_valid_arg(
        self,
        mock_is_valid,
        mock_pk,
        mock_setattr,
        mock_send,
        mock_clear
    ):
        comp = components.Component(CONTEXT)

        mock_is_valid.return_value = True
        mock_pk.return_value = 1

        comp.delete(mock_pk.return_value)

        mock_is_valid.assert_called_with()
        mock_pk.assert_called_with()
        mock_send.assert_called_with(
            client.DELETE,
            comp.ctx(),
            comp.endpoint(),
            None
        )
        mock_clear.assert_called_with()

    @mock.patch('amber_lib.models.components.Component.endpoint')
    @mock.patch('amber_lib.models.components.Component.ctx')
    @mock.patch('amber_lib.client.send')
    @mock.patch('amber_lib.models.components.Component.is_valid')
    def test_delete_pk_invalid(
            self,
            mock_is_valid,
            mock_send,
            mock_ctx,
            mock_endpoint
    ):
        model = components.Component(CONTEXT)
        model.component_data_id = 5

        mock_is_valid.return_value = False

        with self.assertRaises(ValueError):
            model.delete()

    @mock.patch('amber_lib.models.components.Component.endpoint')
    @mock.patch('amber_lib.models.components.Component.ctx')
    @mock.patch('amber_lib.client.send')
    @mock.patch('amber_lib.models.components.Component.is_valid')
    def test_delete_pk_valid_(
            self,
            mock_is_valid,
            mock_send,
            mock_ctx,
            mock_endpoint
    ):
        model = components.Component(Context())
        model.component_data_id = 5

        mock_is_valid.return_value = True

        model.delete()

        self.assertTrue(mock_send.called)
        self.assertTrue(mock_endpoint.called)
        self.assertTrue(mock_ctx.called)

    @mock.patch('amber_lib.models.components.Component.is_valid')
    def test_endpoint_has_no_id(self, mock_is_valid):
        model = components.Component(CONTEXT)
        mock_is_valid.return_value = False

        self.assertEqual(
            model.endpoint(),
            '/components/component'
        )
        mock_is_valid.assert_called_with()

    @mock.patch('amber_lib.models.components.Component.pk')
    @mock.patch('amber_lib.models.components.Component.is_valid')
    def test_endpoint_has_id(self, mock_is_valid, mock_pk):
        comp = components.Component(Context())
        comp.component_data_id = 1
        mock_is_valid.return_value = True
        mock_pk.return_value = 1

        self.assertEqual(
            comp.endpoint(),
            '/components/component/1'
        )
        mock_is_valid.assert_called_with()
        mock_pk.assert_called_with()

    @mock.patch('amber_lib.models.components.client.send')
    def test_form_schema(self, mock_send):
        comp = components.Component(CONTEXT)
        comp._resource = 'component'
        url = "/form_schemas/products?component=%s" % comp._resource

        comp.form_schema()
        mock_send.assert_called_with(
            client.GET,
            comp.ctx(),
            url,
            {}
        )

    @mock.patch('amber_lib.models.components.Component.from_dict')
    @mock.patch('amber_lib.models.components.Component.endpoint')
    @mock.patch('amber_lib.models.components.Component.ctx')
    @mock.patch('amber_lib.client.send')
    def test_retrieve(
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
    def test_save_existing(
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
    def test_save_new(
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
