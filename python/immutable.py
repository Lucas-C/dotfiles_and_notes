# See: http://www.python.org/dev/peps/pep-0416/

# FROM: http://code.activestate.com/recipes/576540/
make_dictproxy = lambda dictobj: type('',(),dictobj).__dict__
# di = make_dictproxy({0:1})
# PROS:
#   d[0] = 42; assert(di[0] == 1)
# CONS:
#   not isinstance(di, dict)
#   ugly __repr__/__str__

# FROM: http://code.activestate.com/recipes/414283-frozen-dictionaries/
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

