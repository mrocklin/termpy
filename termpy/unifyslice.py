from termpy.unification import reify_tuple, unify_seq
#########
# Slice #
#########

def reify_slice(o, s):
    """ Reify a Python ``slice`` object """
    return slice(*reify_tuple((o.start, o.stop, o.step), s))

def unify_slice(u, v, s):
    """ Unify a Python ``slice`` object """
    return unify_seq((u.start, u.stop, u.step), (v.start, v.stop, v.step), s)

from unification import unify_dispatch, reify_dispatch

unify_dispatch[(slice, slice)] = unify_slice
reify_dispatch[slice] = reify_slice
