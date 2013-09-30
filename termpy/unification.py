from functools import partial
from util import transitive_get as walk
from util import assoc
from variable import Var, var, isvar
import itertools as it

from ground import new, op, args, isleaf

################
# Reificiation #
################

def reify_generator(t, s):
    return it.imap(partial(reify, s=s), t)
def reify_tuple(*args):
    return tuple(reify_generator(*args))
def reify_list(*args):
    return list(reify_generator(*args))

def reify_dict(d, s):
    return dict((k, reify(v, s)) for k, v in d.items())

reify_dispatch = {
        tuple: reify_tuple,
        list:  reify_list,
        dict:  reify_dict,
        }

reify_isinstance_list = []

def reify(e, s):
    """ Replace variables of expression with substitution

    >>> from termpy.unification import reify, var
    >>> x, y = var(), var()
    >>> e = (1, x, (3, y))
    >>> s = {x: 2, y: 4}
    >>> reify(e, s)
    (1, 2, (3, 4))

    >>> e = {1: x, 3: (y, 5)}
    >>> reify(e, s)
    {1: 2, 3: (4, 5)}

    """
    if isvar(e):
        return reify(s[e], s) if e in s else e
    elif type(e) in reify_dispatch:
        return reify_dispatch[type(e)](e, s)
    elif not isleaf(e):
        new_op = reify(op(e), s)
        new_args = reify(args(e), s)
        return new(new_op, new_args)
    else:
        return e

###############
# Unification #
###############

def unify_seq(u, v, s):
    if len(u) != len(v):
        return False
    for uu, vv in zip(u, v):  # avoiding recursion
        s = unify(uu, vv, s)
        if s is False:
            return False
    return s

def unify_dict(u, v, s):
    if len(u) != len(v):
        return False
    for key, uval in u.iteritems():
        if key not in v:
            return False
        s = unify(uval, v[key], s)
        if s is False:
            return False
    return s

unify_dispatch = {
        (tuple, tuple): unify_seq,
        (list, list):   unify_seq,
        (dict, dict):   unify_dict,
        }

def unify(u, v, s):  # no check at the moment
    """ Find substitution so that u == v while satisfying s

    >>> from termpy.unification import unify, var
    >>> x = var('x')
    >>> unify((1, x), (1, 2), {})
    {~x: 2}
    """
    u = walk(u, s)
    v = walk(v, s)
    if u == v:
        return s
    elif isvar(u):
        return assoc(s, u, v)
    elif isvar(v):
        return assoc(s, v, u)
    types = (type(u), type(v))
    if types in unify_dispatch:
        return unify_dispatch[types](u, v, s)
    elif not isleaf(u) and not isleaf(v):
        s = unify(op(u), op(v), s)
        if s is False:
            return s
        else:
            return unify(args(u), args(v), s)
    else:
        return False
