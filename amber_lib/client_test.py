from datetime import datetime
import json
import os
import unittest
import urllib
import sys

import mock

from . import api


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

        payload = api.create_payload(ctx, url, data)

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
            api.create_url(ctx, endpoint, **uri),
            self.generate(ctx, endpoint, uri)
        )

    def with_uri_params_test(self):
        ctx = Context()
        endpoint = "products"
        uri = {}

        uri = {"limit": 500, "offset": 3}
        self.assertEqual(
            api.create_url(ctx, endpoint, **uri),
            self.generate(ctx, endpoint, uri)
        )


class Send(unittest.TestCase):
    def using_invalid_method_test(self):
        method = "fubar"
        self.assertRaises(AttributeError, api.send, *[method, None, "", {}])

    @mock.patch('amber_lib.api.requests')
    @mock.patch('amber_lib.api.create_payload')
    @mock.patch('amber_lib.api.create_url')
    def using_valid_method_test(self, mock_url, mock_payload, mock_requests):
        methods = ["get", "post", "put", "delete", "dElEte"]
        get_return = mock.Mock()
        get_return.text = '{"code": "bar", "title": "fubar", "message": "nope"}'
        get_return.status_code = 200

        mock_requests.get = mock.Mock()
        mock_requests.get.return_value = get_return

        for method in methods:
            api.send(method, None, "", {"foo": "bar"})

    """
    @mock.patch('amber_lib.requests.requests')
    @mock.patch('amber_lib.requests.create_payload')
    @mock.patch('amber_lib.requests.create_url')
    def _test(self, mock_url, mock_payload, mock_requests):
        methods = "fubar"

        url = "http://example.com/products?limit=5&offset=100"
        payload = {"signature": "dfAD923jFA3jFA", "data": {}, "url": url}

        mock_url.return_value = url
        mock_payload.return_value = json.dumps(
            payload,
            sort_keys=True,
            separators=(',', ':')
        )
    """



if __name__ == "__main__":
    unittest.main()
