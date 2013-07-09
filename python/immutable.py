# Not pythonic, see: http://www.python.org/dev/peps/pep-0416/

# FROM: http://code.activestate.com/recipes/576540/
# PROS:
#   builtin
# CONS:
#   extra parasite keys : ['__dict__', '__module__', '__weakref__', '__doc__']
#   not isinstance(di, dict)
"""
make_dictproxy = lambda dictobj: type('',(),dictobj).__dict__
"""

# Based on an idea from ThibT: closure poweeer !
# 'Whitelist' approach, real readonly as closure cannot be modified
# Could be made hashable
# CONS
#   not isinstance(make_frozendict({}), dict)
#   make_frozendict({}).__class__ != make_frozendict({}).__class__
import collections
def make_frozendict(original_dict):
    dict_copy = original_dict.copy()
    class frozendict(collections.Mapping):
        def __getitem__(self, key):
            return dict_copy[key]
        def __iter__(self):
            return iter(dict_copy)
        def __len__(self):
            return len(dict_copy)
        def __repr__(self):
            return "frozendict({!r})".format(dict_copy)
    return frozendict()

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
