import collections
import json


class Predicate(object):
    def __init__(self, path, expression):
        self.path = path
        self.expression = expression

    def to_dict(self):
        return {self.path: self.expression}


AND = "&&"
OR = "||"


class _Operator(object):
    def __init__(self, type_, *preds):
        self.type_ = type_
        self.predicates = preds

    def apply(self, pred):
        self.predicates.append(pred)
        return self

    def to_dict(self):
        list_ = []
        for pred in self.predicates:
            if isinstance(pred, (Predicate, And, Or)):
                list_.append(pred.to_dict())
            else:
                raise TypeError()

        return {self.type_: list_}

    def to_json(self):
        return json.dumps(self.to_dict())


class And(_Operator):
    def __init__(self, *preds):
        _Operator.__init__(self, AND, *preds)


class Or(_Operator):
    def __init__(self, *preds):
        _Operator.__init__(self, OR, *preds)


def equal(value):
    return {"==": value}


def not_equal(value):
    return {"!=": value}


def within(value):
    if not isinstance(value, collections.Iterable):
        raise TypeError()
    return {"in": value}


def not_in(value):
    if not isinstance(value, collections.Iterable):
        raise TypeError()
    return {"!in": value}


def min(value):
    return {">=": value}


def max(value):
    return {"<=": value}


def greater_than(value):
    return {">": value}


def less_than(value):
    return {"<": value}


def is_null():
    return {"null": ""}


def is_not_null():
    return {"!null": ""}
