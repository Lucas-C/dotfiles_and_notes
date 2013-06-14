"""""""""""
"" Tricks
"""""""""""
_ # result of the last expression evaluated (in an interpreter only)

r'''Raw string literal: no need to double escape \{0}\{str}'''.format("zero", str="")
u"""Unicode string {obj.__class__} {obj!r}""".format(obj=0)

__slots__ = ("attr1_name")
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

pattern = (
"^"         # beginning of string
"(?P<word>" # named group start
r"\b\w+\b"  # a word between two word separators
")"         # named group end
)
m = re.search(pattern, "Un. Deux. Trois.", re.DEBUG|re.DOTALL|re.MULTILINE)
m.group('word')
# You can also call a function every time something matches a regular expression
re.sub('a|b|c', rep, string) # def rep(matchobj): ...

with open('filea', 'w+') as filea, open('fileb', 'w+') as fileb: pass # touch <files>

# DO NOT use other default parameter values than None, + initialization is static
def foo(x = []):
    x.append('do')
    return x
foo();foo()

it = count().next # itertools

for index, item in enumerate(iterable): ...

os.stat("filename").st_ino # get inode 

from __future__ import print_function
[ print(i) for i in ... ]

datetime.utcnow() # better than time.time()

os.geteuid() == 0 # => run as root

globals()["Foo"] = Foo = type('Foo', (object,), {'bar':True}) # on-the-fly class creation
# Cool alternative for Nose tests, as TestCase and generators are not compatible
# !!WARNING!! 'type()' uses the current global __name__ as the __module__, unless it calls a metaclass constructor
# -> http://stackoverflow.com/questions/14198979/python-inheritance-metaclasses-and-type-function

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

# Descriptors
class Property(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, type):
        if obj is None:
            return self
        return self.fget(obj)

a, b = b, a # swapping

my_list[::-1] == reversed(my_list)
mylist.index(elem) # index lookup

# Cool standard functions to work on lists
zip, reduce, all, any, min, max, sum
# generators > list-comprehensions

dict.iteritems > dict.items
dict.__missing__ # invoked for missing items

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
# or just: e.args += ('More', 'infos')
# also useful: type, value, traceback = sys.exc_info()
else: pass
finally: pass

multiprocessing > threading # as Python can only have on thread because of the GIL

l = ['a,b', 'c,d']
from itertools import chain
s = frozenset(chain.from_iterable(e.split(',') for e in l))

# Callable
hasattr(obj, '__call__') # work for functions too

# Zip archive
foo = zipfile.ZipFile('foo.zip', mode='w')
for root, dirs, files in os.walk('/path/to/foo'):
    for name in files:
        file_to_zip = os.path.join(root, name)
        foo.write(file_to_zip, compress_type=zipfile.ZIP_DEFLATED)


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
# Also:
rom rfoo.utils import rconsole
rconsole.spawn_server()
$ rconsole
# And also:
http://eventlet.net/doc/modules/backdoor.html

# GOTCHAS:
#- http://code.activestate.com/recipes/502271-these-nasty-closures-caveats-for-the-closure-enthu/
#- http://stackoverflow.com/questions/12182068/python-closure-function-losing-outer-variable-access


"""""""""""""""""
"" Libs & tools
"""""""""""""""""
reload(module)

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

# To use 3rd party modules, do not edit PYTHONPATH env var, use *.pth files 


""""""""
"" Fun
""""""""
# Funny loop construct
for ...:
    break
else:

from __future__ import braces

import this
