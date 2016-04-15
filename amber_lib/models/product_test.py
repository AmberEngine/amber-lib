#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import unittest
import sys

import mock

from . import product
from amber_lib import client


class Context(object):
    public = 'mwyclv6bac2lqn9artt1o88laq4muk88483opkp9dnv8289f8olqrxlx7b2s7q8'
    private = "sn4ikxumkpi5dqb0vwo1ujbi68uv3bvoak1p0xzgbzhg71v9p1sn7a2t49dh2tz"
    host = "http://example.com"
    port = "8080"


CONTEXT = Context()


class Product(unittest.TestCase):
    def test_get_components(self):
        prod = product.Product(CONTEXT)
        prod.__dict__['koopa'] = ''
        prod.__dict__['toad'] = ''
        prod.__dict__['_private'] = ''
        prod.__dict__['id'] = ''

        self.assertEqual(len(prod.get_components()), 2)

    @mock.patch('amber_lib.models.components.client.send')
    @mock.patch('amber_lib.models.bases.Model.form_schema')
    @mock.patch('amber_lib.models.product.Product.category')
    def test_form_schema_no_category(
        self,
        mock_cat,
        mock_form_schema,
        mock_send
    ):
        prod = product.Product(CONTEXT)
        mock_cat.primary = None

        url = "/form_schemas/products"

        prod.form_schema()
        mock_form_schema.assert_called_with(prod)

    @mock.patch('amber_lib.models.components.client.send')
    @mock.patch('amber_lib.models.product.Product.category')
    def test_form_schema_has_categories(
        self,
        mock_cat,
        mock_send
    ):
        prod = product.Product(CONTEXT)
        mock_cat.primary = "primary"
        mock_cat.secondary = "secondary"
        mock_cat.tertiary = "tertiary"

        url = "/form_schemas/%s" % prod._resource

        prod.form_schema()

        mock_send.assert_called_with(
            client.GET,
            prod.ctx(),
            url,
            {},
            **{
                "primary": "primary",
                "secondary": "secondary",
                "tertiary": "tertiary"
            }
        )

    @mock.patch('amber_lib.models.product.client.Container')
    @mock.patch('amber_lib.models.bases.client.send')
    def test_search(
        self,
        mock_send,
        mock_container
    ):
        prod = product.Product(CONTEXT)
        filter_ = mock.Mock()
        batch_size = 250
        offset = 42
        uri_args = {"foo": "bar", "fizz": "buzz"}

        prod.search(filter_, batch_size, offset, **uri_args)

        mock_send.assert_called_with(
            client.GET,
            prod._ctx,
            "/products_search",
            {"filtering": filter_.to_dict()},
            limit=batch_size,
            offset=offset,
            **uri_args
        )
