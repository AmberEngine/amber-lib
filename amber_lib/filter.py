import json


class Predicate(object):
    def __init__(self, path, expression):
        self.path = path
        self.expression = expression

    def to_dict(self):
        return {self.path: self.expression}

AND = "and"
OR = "or"

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

        return {"$%s" % self.type_: list_}

    def to_json(self):
        return json.dumps(self.to_dict())

class And(_Operator):
    def __init__(self, *preds):
        _Operator.__init__(self, AND, *preds)

class Or(_Operator):
    def __init__(self, *preds):
        _Operator.__init__(self, OR, *preds)

def equal(value):
    return {"$eq": value}

def not_equal(value):
    return {"$neq": value}

def within(*value):
    if not isinstance(value, tuple):
        raise TypeError()
    return {"$in": value}

def not_in(*value):
    if not isinstance(value, tuple):
        raise TypeError()
    return {"$notIn": value}

def min(value):
    return {"$gte": value}

def max(value):
    return {"$lte": value}

def greater_than(value):
    return {"$gt": value}

def less_than(value):
    return {"$lt": value}

def is_null():
    return {"$null": ""}

def is_not_null():
    return {"$notNull": ""}


