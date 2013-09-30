from contextlib import contextmanager
from termpy.util import hashable
import itertools as it

_global_logic_variables = set()
_glv = _global_logic_variables

class Var(object):
    """ MetaVariable """
    __slots__ = ['token']

    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        return type(self) == type(other) and self.token == other.token

    def __hash__(self):
        return hash((type(self), self.token))

    def __str__(self):
        return '~%s' % self.token
    __repr__ = __str__

var_ids = it.count(1)

def var(*token):
    if len(token) == 0:
        token = "_%s" % next(var_ids)
    elif len(token) == 1:
        token = token[0]
    return Var(token)

vars = lambda n: [var() for i in range(n)]
isvar = lambda t: (isinstance(t, Var) or
                   (not not _glv and hashable(t) and t in _glv))

@contextmanager
def variables(*variables):
    """ Context manager for logic variables

    >>> from __future__ import with_statement
    >>> from termpy import variables, var, isvar
    >>> with variables(1):
    ...     print isvar(1)
    True

    >>> print isvar(1)
    False

    Normal approach

    >>> from termpy import unify
    >>> x = var('x')
    >>> unify((1, x), (1, 2), {})
    {~x: 2}

    Context Manager approach
    >>> with variables('x'):
    ...     print unify((1, 'x'), (1, 2), {})
    {'x': 2}
    """
    old_global_logic_variables = _global_logic_variables.copy()
    _global_logic_variables.update(set(variables))
    try:
        yield
    finally:
        _global_logic_variables.clear()
        _global_logic_variables.update(old_global_logic_variables)
