"""
    This module is intend to be used for debugging purpose.
    Its 'freeze' methods will forbid any future modification of the object or class targetted.

    To do so, it slightly modify the class of the object concerned, only affecting its '__setattr__' method.
    
    type(freeze(o)) == type(o)

    TODO:
        isinstance(freeze(o), o.__class__) # maybe using __subclasshook__ ?

    Original idea: http://code.activestate.com/recipes/576527-freeze-make-any-object-immutable/
"""

class ImmutableException(Exception): pass

def freeze(obj):
    obj.__class__ = _create_immutable_class(obj.__class__)

def is_frozen(obj):
    try:
        return obj.__class__.__setattr__.__module__ == __name__
    except:
        return False

# Using a cache here may give a small perf boost, depending on type() calls cost compared to a dict() lookup
def _create_immutable_class(cls):
    __dict__ = dict(cls.__dict__)
    __dict__['__setattr__'] = __setattr__
    immut_cls = type(cls.__name__, cls.__bases__, __dict__)
    immut_cls.__module__ = cls.__module__
    return immut_cls

def __setattr__(self, attr, value):
    raise ImmutableException("This instance of '{cls}' is frozen, setting attribute '{attr}' to '{value}' is forbidden".format(
        cls=self.__class__, attr=attr, value=value))

