#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import unittest
import sys

import mock

from . import primaries
from amber_lib import client


class Context(object):
    public = 'mwyclv6bac2lqn9artt1o88laq4muk88483opkp9dnv8289f8olqrxlx7b2s7q8'
    private = "sn4ikxumkpi5dqb0vwo1ujbi68uv3bvoak1p0xzgbzhg71v9p1sn7a2t49dh2tz"
    host = "http://example.com"
    port = "8080"


CONTEXT = Context()


class Categories(unittest.TestCase):
    def test_delete(self):
        cat = primaries.Categories(CONTEXT)

        try:
            cat.delete()
        except Exception as e:
            self.fail(e)

    def test_save(self):
        cat = primaries.Categories(CONTEXT)

        try:
            cat.save()
        except Exception as e:
            self.fail(e)


class Option(unittest.TestCase):
    def test_from_dict(self):
        opt = primaries.Option(CONTEXT)

        no_kind = {
            "number": "abc123",
            "default": True,
            "name": "FizzBuzz"
        }

        has_kind = {
            "number": "abc123",
            "default": True,
            "name": "FizzBuzz",
            "kind": "finish"
        }

        is_trim = {
            "number": "abc123",
            "default": True,
            "name": "FizzBuzz",
            "kind": "trim",
            "extended_data": {
                "color": "red",
                "width": 42.23,
                "depth": 634.00
            }
        }

        try:
            opt.from_dict(no_kind)
            opt.from_dict(has_kind)
            opt.from_dict(is_trim)
        except Exception as e:
            self.fail(e)


class SalesChannel(unittest.TestCase):
    @mock.patch('amber_lib.models.primaries.SalesChannel.is_valid')
    def test_related_product_ids_invalid(self, mock_is_valid):
        sc = primaries.SalesChannel(CONTEXT)
        mock_is_valid.return_value = False

        with self.assertRaises(Exception):
            sc.related_product_ids()
        mock_is_valid.assert_called_with()

    @mock.patch('amber_lib.models.primaries.client.send')
    @mock.patch('amber_lib.models.primaries.SalesChannel.pk')
    @mock.patch('amber_lib.models.primaries.SalesChannel.is_valid')
    def test_related_product_ids(self, mock_is_valid, mock_pk, mock_send):
        sc = primaries.SalesChannel(CONTEXT)
        mock_is_valid.return_value = True

        sc.related_product_ids()
        mock_is_valid.assert_called_with()
        mock_pk.assert_called_with()
        mock_send.assert_called_with(
            client.GET,
            sc.ctx(),
            '/relations',
            None,
            sales_channel_id=mock_pk()
        )
