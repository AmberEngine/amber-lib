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


FAKE_DATE = datetime(2015, 11, 30, 22, 36, 52, 538755)
FAKE_DATE_FORMAT = datetime.isoformat(FAKE_DATE)


class Model(unittest.TestCase):
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

    def endpoint(self):
        pass

if __name__ == "__main__":
    unittest.main()
