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


