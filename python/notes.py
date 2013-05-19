"""""""""""
"" Tricks
"""""""""""

__slots__ = ("attr1_name")  # attribute
# Its proper use is "to save space in objects. Instead of having a dynamic dict that allows adding attributes to objects at anytime, there is a static structure which does not allow additions after creation. This saves the overhead of one dict for every object that uses slots."

__all__ = ['bar', 'foo']
# list of symbol to export from module. Default: all symbol not starting with _

__call__
# if a = A(), this is the method called when doing a()

# __repr__ : unambigous, as possible 'eval'uable
"MyClass(this=%r,that=%r)" % (self.this,self.that)

# Funny loop construct
for ...:
    break
else:

code = "my code bla bla"
compiled = compile(code)
exec compiled 

# DO NOT use other default parameter values than None
# + initialization is static
def foo(x = []):
    x.append('do')
    return x
foo()
foo()

datetime.utcnow()
# better than time.time()

globals()["Foo"] = Foo = type('Foo', (object,), {'bar':True})
# on-the-fly class creation
# Cool alternative for Nose tests, as TestCase and generators are not compatible

# 'type' is the metaclass Python uses to create all classes behind the scenes
# aka, the most common __class__.__class__ of an object
# But you can specify your own __metaclass__ !

@patch("module.CONSTANT", new_value)
def foo(): ...

# Functions attributes
def foo(n):
    def inner(i):
        inner.n += i
        return inner.n
    inner.n = n
    return inner

# Decorator with args
def my_decorator(decorator_args):
    def tmp_decorator(orig_func):
        new_func = orig_func
        return new_func
    return tmp_decorator


d == dict(**d)

class Dict(dict):
    def __init__(self, **kwargs):
        self.update(kwargs)
    def __getattr__(self, name):
        return self.get(name)
    def __setattr__(self, name, value):
        self[name] = value


# Signal-based handle on a program to debug
# http://stackoverflow.com/questions/132058/showing-the-stack-trace-from-a-running-python-application

# GOTCHAS:
#- http://code.activestate.com/recipes/502271-these-nasty-closures-caveats-for-the-closure-enthu/
#- http://stackoverflow.com/questions/12182068/python-closure-function-losing-outer-variable-access


"""""""""""""""""
"" Libs & tools
"""""""""""""""""

# HTTP server
python -m SimpleHTTPServer 8080 # --version > 3: -m http.server

# AWESOME for scripting
http://amoffat.github.io/sh/

# PyCharm : code inspection

# get exec time
python -mtimeit -s'xs=range(10)' '[hex(x) for x in xs]' # or 'map(hex, xs)'

# Built-in profiler
python -m cProfile myscript.py
# Visu:
http://www.vrplumber.com/programming/runsnakerun/
https://tech.dropbox.com/2012/07/plop-low-overhead-profiling-for-python/
# And also
http://mg.pov.lt/objgraph/

