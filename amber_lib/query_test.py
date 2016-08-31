import unittest
import unittest.mock as mock

import amber_lib.query as query


class PredicateTests(unittest.TestCase):
    def test__init__(self):
        """Tests instantiating a Predicate object.
        """
        path = 'Product.id'
        expression = {'==', 42}
        p = query.Predicate(path, expression)

        self.assertEqual(p.path, path)
        self.assertEqual(p.expression, expression)

    def test_to_dict(self):
        """Tests calling to_dict() on a Predicate object.
        """
        path = 'Product.id'
        expression = {'>', 1337}
        p = query.Predicate(path, expression)

        print(p.to_dict())
        self.assertTrue(path in p.to_dict())
        self.assertEqual(p.to_dict()[path], expression)


class OperatorTests(unittest.TestCase):
    def test__init__(self):
        """Tests instantiating an Operator object.
        """
        type_ = 'foo'
        preds = ['one', 'two']
        op = query._Operator(type_, *preds)

        self.assertEqual(op.type_, type_)
        self.assertEqual(op.predicates, preds)

    def test_apply(self):
        """Tests calling apply() on an Operator object.
        """
        type_ = 'foo'
        preds = ['one', 'two']
        op = query._Operator(type_, *preds)

        pred = mock.Mock()
        self.assertEqual(op.apply(pred), op)
        self.assertTrue(pred in op.predicates)

    def test_to_dict(self):
        """Tests calling to_dict() on an Operator object.
        """
        type_ = 'foo'
        pred = query.Predicate('Product.id', {'==', 12})
        op = query._Operator(type_, pred)

        expected = {type_: [pred.to_dict()]}
        self.assertEqual(op.to_dict(), expected)

    @mock.patch('amber_lib.query.json.dumps')
    def test_to_json(self, mock_dumps):
        """Tests calling to_json() on an Operator object.
        """
        type_ = 'foo'
        pred = query.Predicate('Product.id', {'==', 12})
        op = query._Operator(type_, pred)

        op.to_json()
        mock_dumps.assert_called_once_with(op.to_dict())


class AndTests(unittest.TestCase):
    @mock.patch('amber_lib.query._Operator.__init__')
    def test__init__(self, mock_init):
        """Tests initializing an And object.
        """
        preds = [mock.Mock(), mock.Mock()]

        a = query.And(*preds)
        mock_init.assert_called_once_with(a, query.AND, *preds)


class OrTests(unittest.TestCase):
    @mock.patch('amber_lib.query._Operator.__init__')
    def test__init__(self, mock_init):
        """Tests initializing an Or object.
        """
        preds = [mock.Mock(), mock.Mock()]

        o = query.Or(*preds)
        mock_init.assert_called_once_with(o, query.OR, *preds)


class HelperTests(unittest.TestCase):
    def test_equal(self):
        """Tests the equal() query method.
        """
        expected = {
            '==': 'test'
        }
        actual = query.equal('test')
        self.assertEqual(expected, actual)

    def test_not_equal(self):
        """Tests the not_equal() query method.
        """
        expected = {
            '!=': 'test'
        }
        actual = query.not_equal('test')
        self.assertEqual(expected, actual)

    def test_within(self):
        """Tests the within() query method when properly called.
        """
        expected = {
            'in': ['test1', 'test2']
        }
        actual = query.within(['test1', 'test2'])
        self.assertEqual(expected, actual)

    def test_within_error(self):
        """
        Tests that within() properly throws an error when called with a
            non-iterable argument.
        """
        with self.assertRaises(TypeError):
            query.within(1337)

    def test_not_in(self):
        """Tests the not_in() query method.
        """
        expected = {
            '!in': [1337, 42]
        }
        actual = query.not_in([1337, 42])
        self.assertEqual(expected, actual)

    def test_not_in_error(self):
        """
        Tests that within() properly throws an error when called with a
            non-iterable argument.
        """
        with self.assertRaises(TypeError):
            query.not_in(1337)

    def test_min(self):
        """Tests the min() query method.
        """
        expected = {
            '>=': 42
        }
        actual = query.min(42)
        self.assertEqual(expected, actual)

    def test_max(self):
        """Tests the max() query method.
        """
        expected = {
            '<=': 1337
        }
        actual = query.max(1337)
        self.assertEqual(expected, actual)

    def test_greater_than(self):
        """Tests the greater_than() query method.
        """
        expected = {
            '>': 42
        }
        actual = query.greater_than(42)
        self.assertEqual(expected, actual)

    def test_less_than(self):
        """Tests the less_than() query method.
        """
        expected = {
            '<': 1337
        }
        actual = query.less_than(1337)
        self.assertEqual(expected, actual)

    def test_is_null(self):
        """Tests the is_null() query method.
        """
        expected = {
            'null': ''
        }
        actual = query.is_null()
        self.assertEqual(expected, actual)

    def test_is_not_null(self):
        """Tests the is_not_null() query method.
        """
        expected = {
            '!null': ''
        }
        actual = query.is_not_null()
        self.assertEqual(expected, actual)
