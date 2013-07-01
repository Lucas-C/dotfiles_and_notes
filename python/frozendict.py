#FROM: http://code.activestate.com/recipes/414283-frozen-dictionaries/

#TODO:
#   - recur_freeze_dls() # dict, list, set -> frozendict, tuple, frozenset + deepcopy if unknown
#   - recur_unfreeze_dls()

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

