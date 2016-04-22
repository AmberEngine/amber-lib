import unittest

import mock

import amber_lib.query as query

class Predicate(unittest.TestCase):
    def test__init__(self):
        path = "Product.id"
        expression = {"==", 42}
        p = query.Predicate(path, expression)

        self.assertEqual(p.path, path)
        self.assertEqual(p.expression, expression)

    def test_to_dict(self):
        path = "Product.id"
        expression = {">", 1337}
        p = query.Predicate(path, expression)

        print(p.to_dict())
        self.assertTrue(path in p.to_dict())
        self.assertEqual(p.to_dict()[path], expression)

class Operator(unittest.TestCase):
    def test__init__(self):
        type_ = "foo"
        preds = ["one", "two"]
        op = query._Operator(type_, *preds)

        self.assertEqual(op.type_, type_)
        self.assertEqual(op.predicates, preds)

    def test_apply(self):
        type_ = "foo"
        preds = ["one", "two"]
        op = query._Operator(type_, *preds)

        pred = mock.Mock()
        self.assertEqual(op.apply(pred), op)
        self.assertTrue(pred in op.predicates)

    def test_to_dict(self):
        type_ = "foo"
        pred = query.Predicate("Product.id", {"==", 12})
        op = query._Operator(type_, pred)

        expected = {type_: [pred.to_dict()]}
        self.assertEqual(op.to_dict(), expected)

    @mock.patch('amber_lib.query.json.dumps')
    def test_to_json(self, mock_dumps):
        type_ = "foo"
        pred = query.Predicate("Product.id", {"==", 12})
        op = query._Operator(type_, pred)

        op.to_json()
        mock_dumps.assert_called_once_with(op.to_dict())


class And(unittest.TestCase):
    @mock.patch('amber_lib.query._Operator.__init__')
    def  test__init__(self, mock_init):
        preds = [mock.Mock(), mock.Mock()]

        a = query.And(*preds)
        mock_init.assert_called_once_with(a, query.AND, *preds)


class Or(unittest.TestCase):
    @mock.patch('amber_lib.query._Operator.__init__')
    def  test__init__(self, mock_init):
        preds = [mock.Mock(), mock.Mock()]

        o = query.Or(*preds)
        mock_init.assert_called_once_with(o, query.OR, *preds)

