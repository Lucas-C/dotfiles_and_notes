"""""""""""
"" Tricks
"""""""""""
# grep-like one-liners:
python -c 'import sys, re; sys.stdout.writelines([str(re.search("REGEX", line).groups())+"\n" for line in sys.stdin])'

_ # result of the last expression evaluated (in an interpreter only)

r'''Raw string literal: no need to double escape \{0}\{str}'''.format("zero", str="")
u"""Unicode string {obj.__class__} {obj!r}""".format(obj=0)
from __future__ import unicode_literals
intern(str) # internal representation

__all__ = ['bar', 'foo']
# list of symbol to export from module. Default: all symbol not starting with _

__slots__ = ("attr1_name")
# Its proper use is "to save space in objects. Instead of having a dynamic dict that allows adding attributes to objects at anytime, there is a static structure which does not allow additions after creation. This saves the overhead of one dict for every object that uses slots." It slightly slow down lookup time

__repr__ # unambigous, as possible 'eval'uable
"MyClass(this=%r,that=%r)" % (self.this,self.that)

__call__
# if a = A(), this is the method called when doing a()

hasattr(obj, '__call__') # isCallable ; work for functions too

def foo(self): return 42
obj.method = types.MethodType( foo, obj ) # binding functions into methods

a, b = b, a # swapping

pattern = (
"^"         # beginning of string
"(?P<word>" # named group start
r"\b\w+\b"  # a word between two word separators
"\.*?"      # non greedy wildcard
")"         # named group end
)
m = re.search(pattern, "Un... Deux... Trois...", re.DEBUG|re.DOTALL|re.MULTILINE)
m.group('word')
# You can also call a function every time something matches a regular expression
re.sub('a|b|c', rep, string) # def rep(matchobj): ...

with open('filea', 'w+') as filea, open('fileb', 'w+') as fileb: pass # touch <files>

StringIO # fake file
# Temp files
tempfile.gettempdir()
tempfile.mkdtemp()
tempfile.NamedTemporaryFile() # file automagically deleted on close()
tempfile.SpooledTemporaryFile(max_size=X) # ditto but file kept in memory as long as siwe < X

os.stat("filename").st_ino # get inode 

# Zip archive
foo = zipfile.ZipFile('foo.zip', mode='w')
for root, dirs, files in os.walk('/path/to/foo'):
    for name in files:
        file_to_zip = os.path.join(root, name)
        foo.write(file_to_zip, compress_type=zipfile.ZIP_DEFLATED)

# DO NOT use other default parameter values than None, + initialization is static
def foo(x = []):
    x.append('do')
    return x
foo();foo()

def bar(**kwargs): # != def bar(foo=None, **kwargs):
    foo = kwargs.pop('foo')

datetime.utcnow() # better than time.time()
import dateutil

os.geteuid() == 0 # => run as root

globals()["Foo"] = Foo = type('Foo', (object,), {'bar':True}) # on-the-fly class creation
# !!WARNING!! 'type()' uses the current global __name__ as the __module__, unless it calls a metaclass constructor
# -> http://stackoverflow.com/questions/14198979/python-inheritance-metaclasses-and-type-function

# It can be an alternative for Nose tests, as TestCase and generators are not compatible
# Better is to simply create in a loop child classes of a parent TestCase that simply redefine the setUp method
# TestCase.subTest is an alternative if data is not common to all test methods in the TestCase
# Even more alternatives : http://stackoverflow.com/questions/2798956/python-unittest-generate-multiple-tests-programmatically

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

class Immut2DPoint(namedtuple('_Immut2DPoint', 'x y')): pass # Immutable class
# Cool namedtuple methods: _asdict(), _replace(kwargs), _fields, namedtuple._make(iterable)

# For multiple inheritance with namedtuple, combine fields + use specific inheritance order:
class Immut3DPoint(namedtuple('_Immut3DPoiint', Immut2DPoint._fields + ('z',)), Immut2DPoint): pass

# !! Beware the Method Resolution Order (cls.__mro__) with 'super' : https://fuhm.net/super-harmful

try: pass
except Exception as err:
    # see chain_errors module
    logging.exception("Additional infos") # Exception will be automagically logged
else: pass
finally: pass

# Environment variables
PYTHONSTARTUP: un module à exécuter au démarrage de Python
PYTHONPATH : une liste de dossiers séparés par ‘:’ qui va être ajouté à sys.path # use *.pth files instead for 3rd party modules
PYTHONHOME : choisir un autre dossier dans lequel chercher l’interpréteur Python.
PYTHONCASEOK : ingorer la casse dans le nom des modules sous Windows
PYTHONIOENCODING : forcer un encoding par défaut pour stdin/stdout/stderr
PYTHONHASHSEED : changer la seed hash() (renforce la sécurité de la VM)


""""""""""""""""""
"" Data structures
""""""""""""""""""
import bisect # binary search
import heapq # min-heap

tuple(obj) # !! PITFALL: fail for None, will parse any sequence like a basestring and won't work on single value
def to_tuple(t):
    if not t:
        return ()
    elif is_sequence(t):
        return tuple(t)
    else:
        return (t,)

l = ['a,b', 'c,d']
from itertools import chain # also has iterator = count().next
s = frozenset(chain.from_iterable(e.split(',') for e in l))

my_list[::-1] == reversed(my_list)
mylist.index(elem) # index lookup

# Cool standard functions to work on lists
zip, reduce, all, any, min, max, sum
# generators > list-comprehensions
def stop(): raise StopIteration
list(e if e != "BREAK" else stop() for e in iterable)

# Is a dict / list ? -> http://docs.python.org/2/library/collections.html#collections-abstract-base-classes
# isinstance(d, collections.Mapping) won't work if the class is not registered, so better check:
hasattr(d, '__getitem__') and hasattr(d, 'keys')

for index, item in enumerate(iterable): ...

# Loop & modify transparently standard DS 
items = zip(xrange(0, len(ds)), ds) # lists, tuples & namedtuples
items = d.iteritems() # dicts ( iteritems > items )


""""""""
"" dict 
""""""""
# Extremely fast as long as < one million elems

collections.OrderedDict # remember insertion order

from itertools import groupby
{category: list(packages) for category, packages in groupby(pkg_list, get_category)} # dict-comprehension, limited: see SO/18664274
{e for e in elems} # set-comprehension

dict.__missing__ # invoked for missing items

assert d == dict(**d)

dict(y, **x) # union of dicts, duplicates are resolved in favor of x

class Bunch(dict): # http://code.activestate.com/recipes/52308
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


"""""""""""
"" Debug
"""""""""""
import nose # -m nose.core -v -w dir --pdb --nologcapture --verbose --nocapture /path/to/test_file:TestCase.test_function
nosetest # -vv --collect-only # for debug
self.assertRaisesRegexp

# IPython tricks
%pdb # Automatic pdb calling

# PDB tricks
debug foo() # step into a function

from pprint import pprint

vars(obj)
dir(obj)

inspect.getmembers(obj)
inspect.getargspec(foo_func) # get signature

<module>.__file__

o.__class__.__bases__ # Get class parents

# http://code.activestate.com/recipes/439096-get-the-value-of-a-cell-from-a-closure/
def get_cell_value(cell): return type(lambda: 0)( (lambda x: lambda: x)(0).func_code, {}, None, None, (cell,) )()
# Example:
def foo(x):
    def bar():
        return x + 'STR_CONST'
    return bar
b = foo(42)
get_cell_value(b.func_closure[0])
b.func_code.co_consts
# Closure GOTCHAS:
#- http://code.activestate.com/recipes/502271-these-nasty-closures-caveats-for-the-closure-enthu/
#- http://stackoverflow.com/questions/12182068/python-closure-function-losing-outer-variable-access

# Signal-based handle on a program to debug
# http://stackoverflow.com/questions/132058/showing-the-stack-trace-from-a-running-python-application
# Also:
from rfoo.utils import rconsole
rconsole.spawn_server()
$ rconsole
# And also:
http://eventlet.net/doc/modules/backdoor.html

code = "my code bla bla"
compiled = compile(code)
exec compiled 

from dis import dis; dis(myfunc) # get dissassembly
uncompyle2 prog.pyc # bytecode -> python code

import gc; gc.get_objects() # Returns a list of all objects tracked by the garbage collector
# SUPER powerful to hack python code and sniff values

# Built-in profiler
python -m cProfile myscript.py # -o output.pstats # cProfile.Profile().dump_stats(filename)
# Visu:
gprof2dot.py -f pstats output.pstats | dot -Tpng -o output.png
pyprof2calltree # use kcachegrind
# And also
https://tech.dropbox.com/2012/07/plop-low-overhead-profiling-for-python/ # like gperftools, sampling profiler for prod servers
http://mg.pov.lt/objgraph # explore Python object graphs

# get exec time
python -mtimeit -s'xs=range(10)' '[hex(x) for x in xs]' # or 'map(hex, xs)'
timeit.timeit("expr", setup="setup code", number=1000)

# Get memory usage
from guppy import hpy
h = hpy()
h.heap()
h.iso(...objects...).sp
# Also: http://stackoverflow.com/questions/938733/total-memory-used-by-python-process
# And: https://pympler.readthedocs.org/en/latest/related.html


"""""""""""""""""""""""""""""
"" Libs & tools for SCIENCE !
"""""""""""""""""""""""""""""
nltk, TextBlob # Text analysis : noun phrase extraction, sentiment analysis, translation...

scipy
    numpy # n-dimensional arrays
    sympy # symbolic mathematics
    pandas # data analysis, to go further : statsmodels, scikit-learn (Machine Learning), orange (dedicated soft for visu)
    maptplotlib # 2d plotting

rpy2 # acces to R


"""""""""""""""""""""
"" Other libs & tools
"""""""""""""""""""""
reload(module)

# Pypy: can be faster, compiles RPython code down to C, automatically adding in aspects such as garbage collection and a JIT compiler

virtualenv # sandbox
pip # or easyinstall : libs manager

json, cPickle # for serialization, the 2nd is a binary format, generic, fast & lighweight

multiprocessing > threading # as Python can only have on thread because of the GIL
numbapro # for CUDA

pyparsing # http://pyparsing.wikispaces.com/HowToUsePyparsing
dakerfp/patterns # AST modification at runtime : real DSL ; http://www.slideshare.net/dakerfp/functional-pattern-matching

pycharm, pylint # code inspection
pyreverse # UML diagrams

http://amoffat.github.io/sh/ # AWESOME for shell scripting

argparse > optparse # or docopt or clize - S&M
group = parser.add_mutually_exclusive_group()
group.add_argument(... type=argparse.FileType('r'))

from getpass import getpass # get password without echoing it

peewee # DB - simple Object Relational Mapping, S&M

beautifulsoup # HTML parsing
bottle # Micro framework web, S&M
HTTPretty # Testing HTTP requests without any server, acting at socket-level
python -m SimpleHTTPServer 8080 # --version > 3: -m http.server
# Basic request parsing:
import re, SimpleHTTPServer, SocketServer
class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        request_match = re.search('param1=([^&]+)', self.path)
        if request_match:
            self.path = param1_match.group(1) + '.json'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
SocketServer.TCPServer(('localhost', 8080), Handler).serve_forever()

paramiko # remote SSH/SFTP connexion

import requests
requests.post('http://urldelamortquitue.com/magicform/', {u'champ1':u"valeur1", u'champ2':u"valeur2"})

mininet # realistic virtual network, running real kernel, switch and application code, on a single machine
socket.inet_aton # validate IP, !! '192.168' is valid

""""""""
"" Fun
""""""""
# Funny loop construct (exist also: try/except/else)
for ...:
    break
else:

from __future__ import braces

import this

a='a=%s;print a%%`a`';print a%`a` # Quine


"""""""""""
" Python 3
"""""""""""
@type_check
def foo(x: between(3, 10), y: is_int) -> is_int:
    return x * y
# Function annotations, see the following SO question that point to PEP 3107 & 0362 (function signatures):
# http://stackoverflow.com/questions/3038033/what-are-good-uses-for-python3s-function-annotations

b'I am an immutable basic byte array of type "bytes"'
bytearray(b"I am mutable")
