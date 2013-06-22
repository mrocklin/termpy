from term.ground import termify
from term import var, unify, reify, variables

class Foo(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __eq__(self, other):
        return (self.a, self.b) == (other.a, other.b)

class Bar(object):
    def __init__(self, c):
        self.c = c
    def __eq__(self, other):
        return self.c == other.c

termify(Foo)

def test_termify():
    x = var()
    assert unify(Foo(1, x), Foo(1, 2), {}) == {x: 2}
    assert reify(Foo(1, x), {x: 2}) == Foo(1, 2)

    # Bar is not a compound term
    assert not unify(Foo(1, Bar(x)), Foo(1, Bar(2)), {})


class Aslot(object):
    __slots__ = ['a', 'b']
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __eq__(self, other):
        return (self.a, self.b) == (other.a, other.b)

termify(Aslot)

def test_termify_slots():
    x = var('x')
    f = Aslot(1, 2)
    g = Aslot(1, x)
    assert unify(f, g, {}) == {x: 2}
    assert reify(g, {x: 2}) == f
