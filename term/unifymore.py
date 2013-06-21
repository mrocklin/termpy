from logpy.unification import (unify_seq, unify_dict, reify_dict, reify_tuple,
        unify_dispatch, reify_dispatch)
from functools import partial

def termify(cls):
    """ Alter a class so that it interacts well with LogPy

    The __class__ and __dict__ attributes are used to define the LogPy term

    See Also:
        _as_term
        _from_term


    >>> from term import termify, var, unify
    >>> class A(object):
    ...     def __init__(self, a, b):
    ...         self.a = a
    ...         self.b = b
    >>> termify(A)

    >>> x = var('x')
    >>> a = A(1, 2)
    >>> b = A(1, x)

    >>> unify(a, b, {})
    {~x: 2}
    """
    if hasattr(cls, '__slots__'):
        cls._as_term = generic_as_term_slot
        cls._from_term = staticmethod(generic_from_term_slot)
    else:
        cls._as_term = generic_as_term_attr
        cls._from_term = staticmethod(generic_from_term_attr)


def generic_as_term_attr(self):
    return (type(self), self.__dict__)


def generic_from_term_attr((typ, attrs)):
    obj = object.__new__(typ)
    obj.__dict__.update(attrs)
    return obj


def generic_as_term_slot(self):
    attrs = dict((attr, getattr(self, attr)) for attr in self.__slots__
                                             if hasattr(self, attr))
    return (type(self), attrs)


def generic_from_term_slot((typ, attrs)):
    obj = object.__new__(typ)
    for attr, val in attrs.items():
        setattr(obj, attr, val)
    return obj
