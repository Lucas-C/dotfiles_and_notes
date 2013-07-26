from collections import Mapping, namedtuple

def issequence(obj):
    return hasattr(obj, '__getitem__') and not isinstance(obj, basestring)

def ismapping(obj):
    return issequence(obj) and hasattr(obj, 'keys')

def freeze(e):
    """
    dict -> namedtuple (!WARNING! keys can only be [a-zA-Z_]+)
    list -> tuple
    """
    if ismapping(e):
        copy = dict(e)
        items = copy.iteritems()
    elif issequence(e):
        copy = list(e)
        items = zip(xrange(0, len(copy)), copy)
    else:
        return e

    for k,v in items:
        copy[k] = freeze(v)

    if ismapping(copy):
        return _dict2NamedTuple(copy)
    elif issequence(copy):
        return tuple(copy)

def unfreeze(e):
    """
    namedtuple -> dict
    tuple -> list
    """
    if hasattr(e, '_asdict'):
        new = e._asdict()
        items = new.iteritems()
    elif issequence(e):
        new = list(e)
        items = zip(xrange(0, len(new)), new)
    else:
        return e

    for k,v in items:
        new[k] = unfreeze(v)

    return new

def _dict2NamedTuple(d):
    NTFromDict = namedtuple('_NTFromDict', d.keys())
    return NTFromDict(**d)


# !WARNING! frozendcit are not pythonic, see: http://www.python.org/dev/peps/pep-0416/

# Based on an idea from ThibT: closure poweeer !
# 'Whitelist' approach, real readonly as closure cannot be modified
# Could be made hashable
# CONS
#   not isinstance(make_frozendict({}), dict)
#   make_frozendict({}).__class__ != make_frozendict({}).__class__
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

# FROM: http://code.activestate.com/recipes/576540/
# PROS:
#   builtin
# CONS:
#   extra parasite keys : ['__dict__', '__module__', '__weakref__', '__doc__']
#   not isinstance(di, dict)
"""
make_dictproxy = lambda dictobj: type('',(),dictobj).__dict__
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

