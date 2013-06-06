"""""""""""
"" Tricks
"""""""""""

r"Raw string literal: no need to double escape \{0}\{str}".format("zero", str="")
u"Unicode string {obj.__class__} {obj!r}".format(obj=0)

dict.iteritems > dict.items

__slots__ = ("attr1_name")  # attribute
# Its proper use is "to save space in objects. Instead of having a dynamic dict that allows adding attributes to objects at anytime, there is a static structure which does not allow additions after creation. This saves the overhead of one dict for every object that uses slots."

__all__ = ['bar', 'foo']
# list of symbol to export from module. Default: all symbol not starting with _

__call__
# if a = A(), this is the method called when doing a()

# __repr__ : unambigous, as possible 'eval'uable
"MyClass(this=%r,that=%r)" % (self.this,self.that)

code = "my code bla bla"
compiled = compile(code)
exec compiled 

with open('<file>', 'w+'): pass # touch <file>

# DO NOT use other default parameter values than None, + initialization is static
def foo(x = []):
    x.append('do')
    return x
foo();foo()

it = count().next # itertools

os.stat("filename").st_ino # get inode 

from __future__ import print_function
[ print(i) for i in ... ]

datetime.utcnow()
# better than time.time()

os.geteuid() == 0 # => run as root

globals()["Foo"] = Foo = type('Foo', (object,), {'bar':True})
# on-the-fly class creation
# Cool alternative for Nose tests, as TestCase and generators are not compatible

# 'type' is the metaclass Python uses to create all classes behind the scenes
# aka, the most common __class__.__class__ of an object
# But you can specify your own __metaclass__ !

@patch("module.open", create=True) # to patch builtins
@patch("module.CONSTANT", new_value)
def foo_test(open_mock):
    input_mock = MagicMock(spec=file)
    open_mock.return_value = input_mock
    input_mock.__enter__.return_value.readline.return_value = "ALWAYS SAME LINE"

# Functions attributes
def foo(n):
    def inner(i):
        inner.n += i
        return inner.n
    inner.n = n
    return inner

# Decorator with args
@functools.wraps
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

# Immutable class
class Immutable(namedtuple('Immutable', 'x y')):
    def __new__(cls, x, y):
        self = super(Immutable, cls).__new__(cls, x, y)
        return self
# Cool namedtuple methods: _asdict(), _replace(kwargs), _fields, namedtuple._make(iterable)

try: pass
except Exception, e: raise MyCustomException("DON'T FORGET TO DISPLAY ROOTCAUSE: {!r}".format(e))
# !!!WARNING!!! -> except OR finally clause, NOT both !

# Better to use multiprocessing lib as Python can only have on thread because of the GIL
def launchWithTimeout(fn, timeout):
    class SigTermException(Exception): pass

    def signal_handler(signum, frame):
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        raise SigTermException

    signal.signal(signal.SIGTERM, signal_handler) 

    def send_sigterm(pid, timeout):
        sleep(timeout)
        os.kill(pid, signal.SIGTERM)

    thread = Thread(target=send_sigterm, args=(os.getpid(), timeout))
    thread.daemon = True
    thread.start()

    try:
        fn()
    except SigTermException:
        pass


l = ['a,b', 'c,d']
from itertools import chain
s = frozenset(chain.from_iterable(e.split(',') for e in l))

# Callable
hasattr(obj, '__call__') # work for functions too


"""""""""""
"" Debug
"""""""""""
import pdb. pdb.set_trace()

from pprint import pprint

vars(obj)
dir(obj)

inspect.getmembers(obj)

<module>.__file__

# Get class parents
o.__class__.__bases__

# Get dissassembly:
from dis import dis
dis(myfunc)

# http://code.activestate.com/recipes/439096-get-the-value-of-a-cell-from-a-closure/
def get_cell_value(cell): return type(lambda: 0)( (lambda x: lambda: x)(0).func_code, {}, None, None, (cell,) )()
# Example:
def foo(x):
    def bar():
        return x
    return bar
b = foo()
get_cell_value(b.func_closure[0])

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

# Serialization
cPickle # binary format, generic, fast & lighweight
json

# Parsing
pyparsing # http://pyparsing.wikispaces.com/HowToUsePyparsing

# AWESOME for shell scripting
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

# Sandbox, libs manager :
virtualenv
pip # or easyinstall
