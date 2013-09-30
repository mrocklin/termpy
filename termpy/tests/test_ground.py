from termpy.ground import new, op, args, isleaf, termify

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


{'a': 1, 'b': 2}
def test_new():
    assert new(tuple, (1,2,3)) == (1,2,3)
    assert new((dict, ('a', 'b')), (1, 2)) == {'a': 1, 'b': 2}
    assert new(Foo, {'a': 1, 'b': 2}) == Foo(1, 2)

def test_op():
    assert op((1,2,3)) == tuple
    assert op({'a': 1, 'b': 2}) == (dict, ('a', 'b'))
    assert op(Foo(1, 2)) == Foo

def test_args():
    assert args((1,2,3)) == (1,2,3)
    assert args({'a': 1, 'b': 2}) == (1, 2)
    assert args(Foo(1, 2)) == {'a': 1, 'b': 2}

def test_isleaf():
    assert isleaf((1,2,3)) == False
    assert isleaf({'a': 1, 'b': 2}) == False
    assert isleaf(Foo(1, 2)) == False
    assert isleaf(1) == True
    assert isleaf(Foo) == True
