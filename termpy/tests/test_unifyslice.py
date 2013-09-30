from termpy import var, unify, reify
from termpy import unifyslice

def test_unify_slice():
    x = var('x')
    y = var('y')

    assert unify(slice(1), slice(1), {}) == {}
    assert unify(slice(1, 2, 3), x, {}) == {x: slice(1, 2, 3)}
    assert unify(slice(1, 2, None), slice(x, y), {}) == {x: 1, y: 2}

def test_reify_slice():
    x = var('x')
    assert reify(slice(1, var(2), 3), {var(2): 10}) == slice(1, 10, 3)

