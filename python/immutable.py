from collections import Mapping, namedtuple
import types

def issequence(obj):
    return hasattr(obj, '__getitem__') and not isinstance(obj, basestring)

def ismapping(obj):
    return issequence(obj) and hasattr(obj, 'keys')

def isset(obj):
    return hasattr(obj, '__contains__') and not isinstance(obj, basestring)

def get_primitive_types():
    primitive_types = {t:getattr(types, t) for t in types.__dict__.keys() if t.endswith('Type') }
    for str_type in types.StringTypes:
        assert issubclass(str_type, basestring)
    primitive_types['StringType'] = basestring
    return primitive_types


def recur_freeze_containers(mutable_obj, ignoredtypes=get_primitive_types().values()):
    """
    dict -> namedtuple (!WARNING! keys can only be [a-zA-Z][a-zA-Z0-9_]*)
    list -> tuple
    set -> frozenset
   """
    if ismapping(mutable_obj):
        copy = dict(mutable_obj)
        items = copy.iteritems()
    elif issequence(mutable_obj):
        copy = list(mutable_obj)
        items = zip(xrange(0, len(copy)), copy)
    elif isset(mutable_obj):
        return frozenset(mutable_obj)
    elif isinstance(mutable_obj, ignoredtypes):
        return mutable_obj 
    else:
        raise TypeError("Cannot freeze {} of unsupported data type {}".format(mutable_obj, type(mutable_obj)))

    for k,v in items:
        copy[k] = recur_freeze_containers(v, ignoredtypes)

    if ismapping(copy):
        return _dict2NamedTuple(copy)
    elif issequence(copy):
        return tuple(copy)

def recur_unfreeze_containers(frozen_obj, ignoredtypes=get_primitive_types().values()):
    """
    namedtuple -> dict
    tuple -> list
    frozenset -> set
    """
    if hasattr(frozen_obj, '_asdict'):
        new = frozen_obj._asdict()
        items = new.iteritems()
    elif issequence(frozen_obj):
        new = list(frozen_obj)
        items = zip(xrange(0, len(new)), new)
    elif isset(frozen_obj):
        return set(frozen_obj)
    elif isinstance(frozen_obj, ignoredtypes):
        return frozen_obj 
    else:
        raise TypeError("Cannot unfreeze {} of unsupported data type {}".format(frozen_obj, type(frozen_obj)))

    for k,v in items:
        new[k] = recur_unfreeze_containers(v, ignoredtypes)

    return new

def _dict2NamedTuple(d):
    NTFromDict = namedtuple('_NTFromDict', d.keys())
    return NTFromDict(**d)


# !WARNING! frozendcit are not pythonic, see: http://www.python.org/dev/peps/pep-0416/

# FROM: http://code.activestate.com/recipes/576540/
# PROS:
#   builtin
# CONS:
#   4 parasite keys : ['__dict__', '__module__', '__weakref__', '__doc__']
#   not isinstance(di, dict)
"""
make_dictproxy = lambda dictobj: type('',(),dictobj).__dict__
"""

# Based on an idea from ThibT: closure poweeer !
# 'Whitelist' approach
# Could be made hashable
# CONS
#   not isinstance(make_frozendict({}), dict)
#   make_frozendict({}).__class__ != make_frozendict({}).__class__
#   NOT REALLY read-only : get_cell_value(di.__getitem__.im_func.func_closure[0]) give access to the mutable dict
"""
def make_frozendict(original_dict):
    dict_copy = original_dict.copy()
    class frozendict(Mapping):
        def __getitem__(self, key):
            return dict_copy[key]
        def __iter__(self):
            return iter(dict_copy)
        def __len__(self):
            return len(dict_copy)
        def __repr__(self):
            return "frozendict({!r})".format(dict_copy)
    return frozendict()
"""

# FROM: http://code.activestate.com/recipes/414283-frozen-dictionaries/
# 'Blacklist' approach
"""
class frozendict(dict):
    def __new__(cls, *args, **kwargs):
        new = dict.__new__(cls)
        dict.__init__(new, *args, **kwargs)
        new._cached_hash = hash(tuple(sorted(new.items())))
        return new

    def __init__(self, *args, **kwargs):
        pass # could be used to modify the frozen dictionary ; ignored because it will be called once on initialization

    def _blocked_attribute(obj):
        raise AttributeError, "A frozendict cannot be modified."
    _blocked_attribute = property(_blocked_attribute)

    __delitem__ = __setitem__ = clear = _blocked_attribute
    pop = popitem = setdefault = update = _blocked_attribute

    def __hash__(self):
        return self._cached_hash

    def __repr__(self):
        return "frozendict({})".format(dict.__repr__(self))
"""

