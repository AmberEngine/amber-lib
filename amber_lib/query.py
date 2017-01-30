import collections
import json


class WhereItem(object):
    def __init__(self, operand="", pred=None, items=None):
        self.operand = operand
        self.pred = pred
        self.items = items if items else []

    def to_dict(self):
        pred = self.pred.to_dict() if self.pred else None
        items = [item.to_dict() for item in self.items]

        return {"operand": self.operand, "pred": pred, "items": items}


    def to_json(self):
        return json.dumps(self.to_dict())


class Predicate(object):
    def __init__(self, subject, operand=None, value=None):
        self.subject = subject
        self.operand = operand
        self.value = value

    def to_dict(self):
        return {"subject": self.subject, "operand": self.operand, "value": self.value}

    def to_json(self):
        return json.dumps(self.to_dict())


class And(WhereItem):
    def __init__(self, first, second, *args):
        super(And, self).__init__()

        children = [second]
        if args:
            children += args

        for index, child in enumerate(children):
            if isinstance(child, Predicate):
                child = WhereItem(pred=second)
            elif not isinstance(child, WhereItem):
                raise TypeError("'%s' must be a Predicate or WhereItem" % child)

            if child.operand and child.operand != "and":
                raise Exception(
                    'WhereItem has operand: %s, must be empty or "%s"' % (
                        child.operand,
                        'and'
                    )
                )
            child.operand = "and"
            children[index] = child

        if isinstance(first, Predicate):
            self.operand = ""
            self.pred = first
            self.items = children
        elif isinstance(first, WhereItem):
            if not first.items:
                self.items += first.items + children
        else:
            raise TypeError("'%s' must be a Predicate or WhereItem" % first)


class Or(WhereItem):
    def __init__(self, first, second, *args):
        super(And, self).__init__()

        children = [second]
        if args:
            children += args

        for index, child in enumerate(children):
            if isinstance(child, Predicate):
                child = WhereItem(pred=second)
            elif not isinstance(child, WhereItem):
                raise TypeError("'%s' must be a Predicate or WhereItem" % child)

            if child.operand and child.operand != "or":
                raise Exception(
                    'WhereItem has operand: %s, must be empty or "%s"' % (
                        child.operand,
                        'or'
                    )
                )
            child.operand = "or"
            children[index] = child

        if isinstance(first, Predicate):
            self.operand = ""
            self.pred = first
            self.items = children
        elif isinstance(first, WhereItem):
            if not first.items:
                self.items += first.items + children
        else:
            raise TypeError("'%s' must be a Predicate or WhereItem" % first)


