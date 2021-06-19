
class Variable(int):
    truthy = True

    def __new__(cls, v):
        assert v > 0
        return super(cls, cls).__new__(cls, v)

    def __neg__(self):
        return -Literal(self)

    @property
    def variable(self):
        return self


class Literal(int):
    def __new__(cls, v):
        assert v != 0
        return super(cls, cls).__new__(cls, v)

    def __neg__(self):
        return Literal(-int(self))

    @property
    def truthy(self):
        return self > 0

    @property
    def variable(self):
        return Variable(abs(self))
