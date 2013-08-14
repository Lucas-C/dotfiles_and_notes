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

# 'Whitelist' approach
# Credits :
#   Thibault Toledano for the original closure idea
#   http://code.activestate.com/recipes/576540/
# PROS
#   really read-only as values in closures cannot be re-assigned (see below)
#   use a builtin data structure
#   dict(make_frozendict(a_dict)) == a_dict
#   the object passed as a parameter doesn't need to be a dict, just to support dict "cast", and an additionnal copy will then be made
#       e.g. make_frozendict(make_frozendict(a_dict))
# CONS
#   4 blacklisted keys
#   make_frozendict({}).__class__ != make_frozendict({}).__class__
#   not isinstance(make_frozendict({}), dict)
# EXTENSIONS
#   could be made hashable
#   could implement items/iteritems more efficiently (collections.Mapping return (key, self[key]), which cost a lookup each time)

_DICTPROXY_EXTRA_KEYS = tuple(type('',(),{}).__dict__.keys())
def make_frozendict(original_dict):
    if not isinstance(original_dict, dict):
        original_dict = dict(original_dict)
    for key in _DICTPROXY_EXTRA_KEYS:
        if key in original_dict:
            raise ValueError("frozendict cannot contain '{}' as a key (blacklisted keys : {})".format(key, _DICTPROXY_EXTRA_KEYS)) 
    dict_proxy = type('',(),original_dict).__dict__
    class frozendict(Mapping):
        def __getitem__(self, key):
            if key in _DICTPROXY_EXTRA_KEYS:
                raise KeyError(key)
            return dict_proxy[key]
        def __iter__(self):
            return (k for k in dict_proxy if k not in _DICTPROXY_EXTRA_KEYS)
        def __len__(self):
            return len(dict_proxy) - len(_DICTPROXY_EXTRA_KEYS)
        def __repr__(self):
            return "make_frozendict({!r})".format({k:self[k] for k in self})
    return frozendict()


# Closure are not writable:
#   foo.func_closure = None # TypeError: readonly attribute
#   foo.func_closure[0] = None # TypeError: 'tuple' object does not support item assignment
#   foo.func_closure[0].cell_contents = None # AttributeError: attribute 'cell_contents' of 'cell' objects is not writable

