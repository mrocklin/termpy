from functools import partial

nth = lambda i: lambda seq: seq[i]
first = nth(0)
second = nth(1)


seq = {'new':   lambda op, args: op(args),
       'op':    lambda term: type(term),
       'args':  lambda term: tuple(term),
       'isleaf':lambda term: False}

term_registry = {
    dict:  {'new':   lambda keys, args: dict(zip(keys, args)),
            'op':    lambda term: (type(term), tuple(sorted(term.keys()))),
            'args':  lambda term: tuple(map(second, sorted(term.items()))),
            'isleaf':lambda term: False},
    list: seq,
    tuple: seq
    }


def new(op, args):
    if isinstance(op, type) and issubclass(op, (tuple, list)):
        return op(args)
    if isinstance(op, tuple) and issubclass(op[0], dict):
        keys = op[1]
        return op[0](zip(keys, args))
    if op in term_registry:
        return term_registry[op]['new'](args)
    if hasattr(op, '_term_new'):
        return op._term_new(args)
    raise NotImplementedError()

def make(fnname, term):
    typ = type(term)
    if typ in term_registry:
        return term_registry[typ][fnname](term)
    methodname = '_term_'+fnname
    if hasattr(term, methodname):
        return getattr(term, methodname)()
    raise NotImplementedError()

op = partial(make, 'op'); op.func_name = 'op'
args = partial(make, 'args'); op.func_name = 'args'

def isleaf(term):
    typ = type(term)
    if typ in term_registry:
        return term_registry[typ]['isleaf'](term)
    if hasattr(term, '_term_isleaf') and not isinstance(term, type):
        return getattr(term, '_term_isleaf')()
    return True

def attr_new(op, args):
    obj = object.__new__(op)
    obj.__dict__.update(args)
    return obj
def attr_op(term):
    return type(term)
def attr_args(term):
    return term.__dict__
def attr_isleaf(term):
    return False

def termify_attr(cls):
    cls._term_new = classmethod(attr_new)
    cls._term_op = attr_op
    cls._term_args = attr_args
    cls._term_isleaf = attr_isleaf
    return cls

def slot_new(op, args):
    obj = object.__new__(op)
    for slot, arg in zip(op.__slots__, args):
        setattr(obj, slot, arg)
    return obj
def slot_op(term):
    return type(term)
def slot_args(term):
    return tuple(map(term.__getattribute__, term.__slots__))
def slot_isleaf(term):
    return False

def termify_slot(cls):
    cls._term_new = classmethod(slot_new)
    cls._term_op = slot_op
    cls._term_args = slot_args
    cls._term_isleaf = slot_isleaf
    return cls

def termify(cls):
    if hasattr(cls, '__slots__'):
        return termify_slot(cls)
    else:
        return termify_attr(cls)
