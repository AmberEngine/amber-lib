from datetime import datetime
import json
import os
import unittest
import urllib
import sys

import mock

from . import client


class Context(object):
    public = 'mwyclv6bac2lqn9artt1o88laq4muk88483opkp9dnv8289f8olqrxlx7b2s7q8'
    private = "sn4ikxumkpi5dqb0vwo1ujbi68uv3bvoak1p0xzgbzhg71v9p1sn7a2t49dh2tz"
    host = "http://example.com"
    port = "8080"


FAKE_DATE = datetime(2015, 11, 30, 22, 36, 52, 538755)
FAKE_DATE_FORMAT = datetime.isoformat(FAKE_DATE)


class CreatePayload(unittest.TestCase):
    @mock.patch('amber_lib.datetime')
    def create_json_payload_test(self, mock_datetime):
        ctx = Context()
        mock_datetime.utcnow.return_value = FAKE_DATE
        mock_datetime.isoformat.return_value = FAKE_DATE_FORMAT

        url = "%s:%s/fake_resource" % (ctx.host, ctx.port)
        data = {"foo": "bar"}

        payload = client.create_payload(ctx, url, data)

        self.assertIsNotNone(payload)
        self.assertGreater(len(json.loads(payload)), 0)


class CreateURL(unittest.TestCase):
    def generate(self, ctx, end, params):
        url = "%s:%s/%s" % (ctx.host, ctx.port, end)
        if len(params) > 0:
            url += "?"
            url += "&".join(["%s=%s" % (k, v) for k, v in params.items()])
        return url

    def no_uri_params_test(self):
        ctx = Context()
        endpoint = "products"
        uri = {}

        self.assertEqual(
            client.create_url(ctx, endpoint, **uri),
            self.generate(ctx, endpoint, uri)
        )

    def with_uri_params_test(self):
        ctx = Context()
        endpoint = "products"
        uri = {}

        uri = {"limit": 500, "offset": 3}
        self.assertEqual(
            client.create_url(ctx, endpoint, **uri),
            self.generate(ctx, endpoint, uri)
        )


class Send(unittest.TestCase):
    def using_invalid_method_test(self):
        method = "fubar"
        self.assertRaises(AttributeError, client.send, *[method, None, "", {}])

    @mock.patch('amber_lib.client.requests')
    @mock.patch('amber_lib.client.create_payload')
    @mock.patch('amber_lib.client.create_url')
    def using_valid_method_test(self, mock_url, mock_payload, mock_requests):
        methods = ["get", "post", "put", "delete", "dElEte"]
        return_mock = mock.Mock()
        return_mock.text = '{"code": "bar", "title": "fubar", "message": "nope"}'
        return_mock.status_code = 200


        for method in methods:
            m = mock.Mock()
            m.return_value = return_mock
            setattr(mock_requests, method, m)

            client.send(method, None, "", {"foo": "bar"})


    @mock.patch('amber_lib.client.requests')
    @mock.patch('amber_lib.client.create_payload')
    @mock.patch('amber_lib.client.create_url')
    def not_200_status_test(self, mock_url, mock_payload, mock_requests):
        method = "get"
        return_mock = mock.Mock()
        return_mock.text = '{"code": "bar", "title": "fubar", "message": "nope"}'
        return_mock.status_code = 418

        m = mock.Mock()
        m.return_value = return_mock
        setattr(mock_requests, method, m)

        self.assertRaises(Exception, client.send, *[method, None, "", {}])


if __name__ == "__main__":
    unittest.main()
