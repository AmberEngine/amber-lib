import unittest

import amber_lib.connection as connection
import amber_lib.models.bases as bases
import amber_lib.models.components as components
import amber_lib.models.primaries as primaries


class Connection(unittest.TestCase):
    def dunder_enter_test(self):
        dict_ = {}

        conn1 = connection.Connection({})
        with conn1 as conn2:
            self.assertEqual(conn2, conn1)

    def dunder_exit_test(self):
        conn = connection.Connection({})
        self.assertEqual(conn.__exit__(None, None, None), None)

    def dunder_getattr_valid_model_test(self):
        conn = connection.Connection({})
        self.assertTrue(isinstance(conn.Model, bases.Model))

    def dunder_getattr_name_collision_primary_test(self):
        conn = connection.Connection({})
        self.assertTrue(isinstance(conn.Manufacturer, primaries.Manufacturer))

    def dunder_getattr_name_collision_component_test(self):
        conn = connection.Connection({})
        self.assertTrue(
            isinstance(
                conn.components.Manufacturer,
                components.Manufacturer
            )
        )

    def dunder_getattr_invalid_model_test(self):
        conn = connection.Connection({})
        self.assertRaises(AttributeError, lambda: conn.DoesntExistModel)

    def dunder_init_test(self):
        dict_ = {'foo': 'bar', 'fizz': 'buzz'}

        conn = connection.Connection(dict_)
        self.assertEqual(conn.context, dict_)
