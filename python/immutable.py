"""
    This module is intend to be used for debugging purpose.
    Its 'freeze' methods will forbid any future modification of the object or class targetted.

    On objects, it replaces their class by an almost entirely identical one,
    with its setters triggering an error.
    
    HOWEVER, for frozen objects:
        type(frozen_o) != type(orig_o)
        not isinstance(frozen_o, orig_o.__class__)

    Freezing a class will only work if it already has a __setattr__ magic method.
    Also, no more instances of a frozen can be instantiated.

    Original idea: http://code.activestate.com/recipes/576527-freeze-make-any-object-immutable/
"""

class ImmutableException(Exception): pass

def freeze(obj):
    new_dict = dict(obj.__class__.__dict__)
    new_dict['__setattr__'] = _err('__setattr__')
    obj.__class__ = _create_class_copy(obj.__class__, new_dict)

def freeze_class(cls):
    cls.__setattr__ = _err('__setattr__')

def is_frozen(obj_or_cls):
    answer = False
    try: answer = (obj_or_cls.__class__.__setattr__.__module__ == __name__)
    except: pass
    try: answer = (obj_or_cls.__setattr__.__module__ == __name__)
    except: pass
    return answer

# Using a cache here to store already created frozen classes may give a small perf boost
def _create_class_copy(cls, new_dict):
    try:
        metaclass = cls.__metaclass__
    except:
        metaclass = type
    copy_cls = metaclass(cls.__name__, cls.__bases__, new_dict)
    copy_cls.__module__ = cls.__module__
    return copy_cls

def _err(fn_name):
    def err_fn(self, *args, **kwargs):
        raise ImmutableException("This instance of '{cls}' is frozen, calling {fn}({args}, {kwargs})' is forbidden".format(
            cls=self.__class__, fn=fn_name, args=args, kwargs=kwargs))
    return err_fn

