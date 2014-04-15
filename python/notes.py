"""""""""""
"" Tricks
"""""""""""
# grep-like one-liners:
python -c 'import sys, re; sys.stdout.writelines([str(re.search("REGEX", line).groups())+"\n" for line in sys.stdin])'

_ # result of the last expression evaluated (in an interpreter only)

r'''Raw string literal: no need to double escape \{0}\{one:.5f}'''.format("zero", one=1)
u"""Unicode string {obj.__class__} {obj!r}""".format(obj=0)
from __future__ import unicode_literals
intern(str) # internal representation - useful for enums/atoms

__all__ = ['bar', 'foo']
# list of symbol to export from module. Default: all symbol not starting with _

__slots__ = ("attr1_name")
# Its proper use is "to save space in objects. Instead of having a dynamic dict that allows adding attributes to objects at anytime, there is a static structure which does not allow additions after creation. This saves the overhead of one dict for every object that uses slots." It slightly slow down lookup time

__repr__ # unambigous, as possible 'eval'uable
"MyClass(this=%r,that=%r)" % (self.this,self.that)

hasattr(obj, '__call__') # isCallable ; work for functions too

a, b = b, a # swapping

pattern = (
"^"         # beginning of string
"(?P<word>" # named group start
r"\b\w+\b"  # a word between two word separators
"\.*?"      # non greedy wildcard
")"         # named group end
)
m = re.search(pattern, "Un... Deux... Trois...", re.DOTALL|re.MULTILINE) # re.DEBUG -> print parse tree
m.group('word')
# You can also call a function every time something matches a regular expression
re.sub('a|b|c', rep_func, string) # def rep_func(matchobj): ... - More powerful than str.replace for substitutions

with open('filea', 'rb+', buffering=0) as inf, io.open('fileb', 'wU', encoding='utf-8') as outf: pass # touch 'fileb'

def CtxtMgr(object):
    def __enter__(self): pass
    def __exit__(self, eType, eValue, eTrace): pass
@contextlib.contextmanager
def foobar():
    # __enter__ code
    yield
    # __exit__ code

StringIO # fake file

tempfile.gettempdir()
tempfile.mkdtemp()
tempfile.NamedTemporaryFile() # file automagically deleted on close()
tempfile.SpooledTemporaryFile(max_size=X) # ditto but file kept in memory as long as size < X

glob, fnmatch # manipulate unix-like file patterns
os.stat("filename").st_ino # get inode
.st_size # in bytes. Human readable size: http://stackoverflow.com/q/1094841/636849

from distutils import spawn
cmd_path = spawn.find_executable('cmd') # shutil.which in Python3
subprocess.check_output([cmd_path, 'do', 'stuff'], stderr=STDOUT)
# AVOID PIPE ! Flaws & workarounds: http://www.macaronikazoo.com/?p=607 ; http://eyalarubas.com/python-subproc-nonblock.html

# DO NOT use other default parameter values than None, + initialization is static
def foo(x = []):
    x.append('do')
    return x
foo();foo()

def bar(**kwargs): # != def bar(foo=None, **kwargs):
    foo = kwargs.pop('foo')

datetime.utcnow() # better than time.time()
import pytz # pytz.utc, pytz.all_timezones
from dateutil import parser # !! ALWAYS pass a Callable as tzinfos so that it won't use the system timezone (time.tzname)
def _tzinfos_pytz_pst_func(tzname, tzoffset):
    tzdata = pytz.timezone('America/Los_Angeles') if tzname == 'PST' else pytz.timezone(tzname)
    if tzoffset:
        tzdata += timedelta(seconds=tzoffset)
    return tzdata

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

dir(__builtins__) # special module, and functions can be reassigned !
@patch("module.open", create=True) # to patch builtins
@patch("module.CONSTANT", new_value)
def foo_test(open_mock):
    input_mock = MagicMock(spec=file)
    open_mock.return_value = input_mock
    input_mock.__enter__.return_value.readline.return_value = "ALWAYS SAME LINE"

obj_mock.side_effect = Exception('Foo42')

def incr(i):
    incr.counter += i
    return incr.counter
inner.counter = 0 # Function attribute
obj.method = types.MethodType(function, obj) # binding functions into methods

# Decorator with args (deep dive on them on http://blog.dscpl.com.au)
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

buffer & memoryview

class Immut2DPoint(namedtuple('_Immut2DPoint', 'x y')): pass # Immutable class
# Cool namedtuple methods: _asdict(), _replace(kwargs), _fields, namedtuple._make(iterable)

# For multiple inheritance with namedtuple, combine fields + use specific inheritance order:
class Immut3DPoint(namedtuple('_Immut3DPoiint', Immut2DPoint._fields + ('z',)), Immut2DPoint): pass

# !! Beware the Method Resolution Order (cls.__mro__) with 'super' : https://fuhm.net/super-harmful

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(process)s [%(levelname)s] %(filename)s %(lineno)d %(message)s")
logging.handlers.[Timed]RotatingFileHandler # logrotate in Python
try: Ellipsis # like 'pass' but as an object, not a statement
except Exception as err:
    # see chain_errors module
    logging.exception("Additional infos") # Exception will be automagically logged
    import traceback; traceback.print_exc() # or .extract_stack()
else: pass
finally: pass

from distutils.command.build import build
class custom_build(build):
    def run(self):
        build.run(self)
        ... # custom init
cmdclass['build'] = custom_build

# Environment variables
PYTHONSTARTUP: un module à exécuter au démarrage de Python
PYTHONPATH : une liste de dossiers séparés par ‘:’ qui va être ajouté à sys.path # use *.pth files instead for 3rd party modules - See also: import site
PYTHONHOME : choisir un autre dossier dans lequel chercher l’interpréteur Python.
PYTHONCASEOK : ingorer la casse dans le nom des modules sous Windows
PYTHONIOENCODING : forcer un encoding par défaut pour stdin/stdout/stderr
PYTHONHASHSEED : changer la seed hash() (renforce la sécurité de la VM)

zip -r ../myapp.egg # Make an .egg - You just need a ./__main__.py - See also: zipimport, pkgutil


""""""""""""""""""
"" Data structures
""""""""""""""""""
import bisect # binary search
import heapq # min-heap: .nlargest .nsmallest

collections.deque # double-ended queue, with optional maximum length

collections.Counter([...]).most_common(1) # dict subclass for integer values
unique_id_map = collections.defaultdict(itertools.count().next) # will always return the same unique int when called on an object: unique_id_map['a'] == unique_id_map['a'] != unique_id_map['b']

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
array # > list for large data sets, but imply all elements have same basic type (char, int...)

group_adjacent = lambda a, k: zip(*(a[i::k] for i in range(k))) # [(1, 2, 3), (4, 5, 6)]

def n_grams(a, n): # sliding window: [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6)]
    z = [iter(a[i:]) for i in range(n)]
    return zip(*z)

# Cool standard functions to work on lists
zip, reduce, all, any, min, max, sum
# generators > list-comprehensions
def stop(): raise StopIteration
list(e if e != "BREAK" else stop() for e in iterable)
class CustomGenerator(object): # minimal generator protocol
    def __iter__(self):
        yield stuff
        #OR
        return self # then must implement 'next(self)' (__next__ in Python3)

# Is a dict / list ? -> http://docs.python.org/2/library/collections.html#collections-abstract-base-classes
# isinstance(d, collections.Mapping) won't work if the class is not registered, so better check:
hasattr(d, '__getitem__') and hasattr(d, 'keys')

for index, item in enumerate(iterable): ...

# Loop & modify transparently standard DS
items = zip(xrange(0, len(ds)), ds) # lists, tuples & namedtuples
items = d.iteritems() # dicts ( iteritems > items )


"""""""""""""
"" dict & set
"""""""""""""
# Extremely fast as long as < one million elems

collections.OrderedDict # remember insertion order
OrderedDict(sorted(d.iteritems(), key=lambda (k,v): (v,k))) # sort a dict by its values

from itertools import groupby
{category: list(packages) for category, packages in groupby(pkg_list, get_category)} # dict-comprehension, limited: see SO/18664274
{e for e in elems} # set-comprehension

set operators : | & - ^

dict.__missing__ # invoked for missing items

assert d == dict(**d)

dict(y, **x) # union of dicts, duplicates are resolved in favor of x

class Bunch(dict): # or inherit from defaultdict - http://code.activestate.com/recipes/52308
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

def sets_converter(obj): list(obj) if isinstance(obj, set) else obj.__dict__ # or pass custom json.JSONEncoder as the 'cls' argument to 'dumps'
json.dumps(d, sort_keys=True, indent=4, default=sets_converter) # pretty formatting - Also: -mjson.tool

# Tricky gotcha
d = {'a':42}
print type(d.keys()[0]) # str
class A(str): pass
a = A('a')
d[a] = 42
print d # {'a':42}
print type(d.keys()[0]) # str


"""""""""""""""""
"" Test & Debug
"""""""""""""""""
faulthandler.enable() # dump stacktrace on SIGSEGV, SIGABRT... signals ; python2 -X faulthandler script.py

import nose # -m nose.core -v -w dir --pdb --nologcapture --verbose --nocapture /path/to/test_file:TestCase.test_function
nosetest # -vv --collect-only # for debug
self.assertRaisesRegexp / assertDictContainsSubset / assertAlmostEqual(expected, measured, places=7)
import sure # use assertions like 'foo.when.called_with(42).should.throw(ValueError)'
import doctest # include tests as part of the documentation

# IPython tricks
cd /a/path
!cmd # shell command
%history # dump it
%pdb # Automatic pdb calling
%timeit do_something()
%debug # post_mortem
%bg # run in the background
ipython nbconvert --to [html|latex|slides|markdown|rst|python]

# PDB tricks
debug foo() # step into a function with pdb
import pdb; foo(42); pdb.pm() # enter debugger post-mortem
from IPython.core.debugger import Pdb; Pdb().set_trace()
ipdb.set_trace() / python -mipdb / ipdb.pm() / ipdb.runcall(function, arg)
google/pyringe # when python itself crashes, gets stuck in some C extension, or you want to inspect data without stopping a program

from pprint import pprint # indent=4

vars(obj)
dir(obj)

inspect.getmembers(obj)
inspect.getargspec(foo_func) # get signature
inspect.getfile(my_module)
frame,filename,line_number,function_name,lines,index=inspect.getouterframes(inspect.currentframe())[1]

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
#- http://stackoverflow.com/q/12182176

pids = subprocess.check_output(['pgrep', '-f', 'process_pattern']).splitlines() # more portable ? -> psutil
for pid in pids:
    os.kill(int(pid), signal.SIGTERM)
# Pitfalls of signals: http://thisismiller.github.io/blog/CPython-Signal-Handling/
# Signal-based handle on a program to debug: http://stackoverflow.com/a/133384/636849
from rfoo.utils import rconsole
rconsole.spawn_server()
$ rconsole
# And also: http://eventlet.net/doc/modules/backdoor.html

code = "my code bla bla"
compiled = compile(code)
exec compiled

from dis import dis; dis(myfunc) # get dissassembly
uncompyle2 prog.pyc # bytecode -> python code

import gc; gc.get_objects() # Returns a list of all objects tracked by the garbage collector
# SUPER powerful to hack python code and sniff values

python -m cProfile myscript.py -o output.pstats # cProfile.Profile().dump_stats(filename)
gprof2dot.py -f pstats output.pstats | dot -Tpng -o output.png
kernprof.py --line-by-line myscript.py # line_profiler
pyprof2calltree # use kcachegrind
https://tech.dropbox.com/2012/07/plop-low-overhead-profiling-for-python/ # like gperftools, sampling profiler for prod servers
http://mg.pov.lt/objgraph # explore Python object graphs

python -mtimeit -s'xs=range(10)' '[hex(x) for x in xs]' # exec time, compare to 'map(hex, xs)'
timeit.timeit(lambda: local_func(), setup="from m import dostuff; dostuff()", number=1000)

# Get memory usage
from guppy import hpy
h = hpy()
h.heap()
h.iso(...objects...).sp
# Also: http://stackoverflow.com/questions/938733/total-memory-used-by-python-process
# And: https://pympler.readthedocs.org/en/latest/related.html - asizeof is the simplest one
import tracemalloc # Python3

def get_refcount(obj):
    """Valid for CPython implementation only"""
    return ctypes.c_size_t.from_address(id(obj))
# FUN FACT: the references to the 'int' [-5 ; 256] are shared


"""""""""""""""""""""""""""""
"" Libs & tools for SCIENCE !
"""""""""""""""""""""""""""""
nltk, TextBlob # Text analysis : noun phrase extraction, sentiment analysis, translation...
topia.termextract
difflib # compare sequences

decimal.Decimal # contrary to floats : 3*0.1 - 0.3 == 0.0
float("inf") # infinite !
fractions
statistics # Python 3

scipy
    numpy # n-dimensional arrays
    sympy # symbolic mathematics: formula printing (also: PyLatex), simplification, equations, matrices, solvers...
    pandas # data analysis, to go further : statsmodels, scikit-learn (Machine Learning), orange (dedicated soft for visu)
    matplotlib, prettyplotlib, mpld3 # 2d plotting

SimpleCV # powerful computer vision tools : find image edge, keypoints, morphology; can use the Kinect
networkx # networks & graphs manipulation

mmap
joblib # memoize computations by keeping cache files on disk

rpy2 # acces to R

from cryptography.fernet import Fernet # symmetric encryption


"""""""""""""""""""""
"" Other libs & tools
"""""""""""""""""""""
reload(module)

Pypy # can be faster, compiles RPython code down to C, automatically adding in aspects such as garbage collection and a JIT compiler
Jython / Py4J # intercommunicate with Java

virtualenv # sandbox
pip # or easyinstall : libs manager

multiprocessing, Pyro > threading # as Python can only have on thread because of the GIL + using multiprocessing => everything should be pickable
threading.Thread().deamon = True # The entire Python program exits when no alive non-daemon threads are left.
threading.Event # for threads communication, including stopping: Thread.run(self): while not self.stop_event: ...
# Kill a thread ? -> http://stackoverflow.com/a/325528/636849
from multiprocessing.dummy import Pool as ThreadPool
pool = ThreadPool(4); results = pool.map(foo, args); pool.close(); pool.join()

select # efficient I/O
def _make_file_read_nonblocking(f):
    fd = f.fileno()
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
greenlets/gevent, Stackless, libevent, libuv, Twisted, Tornado, asyncore # other ASync libs, that is :
# concurrency (code run independently of other code) without parallelism (simultaneous execution of code)
@asyncio.couroutine # aka Tulip, std in Python 3.3, port for Python 2.7 : trollius
numbapro # for CUDA

autobanh # meteor.js in Python
asynchat, irc
mailr, mailbox, imaplib, smtpd, smptplib

celery # distributed task queue ; alt: pyres
sched # event scheduler ; alt: dagobah/schedule
zeromq, aiozmq  # distributed app / msg passing framework

mrjob, luigi # Hadoop / AWS map-reduce jobs

pyparsing # http://pyparsing.wikispaces.com/HowToUsePyparsing
dakerfp/patterns # AST modification at runtime : real DSL ; http://www.slideshare.net/dakerfp/functional-pattern-matching

pylama # include pyflakes, pylint, PEP-checking - Also: Flake8
pyreverse # UML diagrams

http://amoffat.github.io/sh/ # AWESOME for shell scripting
shlex.split('--f "a b"') # tokenize parameters properly

def function_with_docstring(foo): # sphinx
    """Do this and that, similar to :func:`a_function_name`
    Used in module :mod:`amodulename`
    :param foo: Something
    :type count: :class:`MyClass`
    :returns: True if users are happy
    :rtype: boolean
    :raises: KeyError
    """
    return False

argparse > optparse # or docopt or clize - S&M
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(... type=argparse.FileType('r'))

from getpass import getpass # get password without echoing it
pyreadline, readline, rlcompleter
colorama # cross-platform colored terminal text
tqdm # KISS progress bar

@retry # https://github.com/rholder/retrying

import uuid # generate unique ID’s

resource # limit a process resources: SPU time, heap size, stack size...

peewee, SQLAlchemy # ORM DB
anydbm: dbhash else gdbm else dbm else dumbdbm
sqlite3 # std DB, persistent in a file || can be created in RAM
shelve # other data persistence using pickle, full list of alt: http://docs.python.org/2/library/persistence.html

ConfigParser # std configuration files format
csv, json, cPickle # for serialization, the 2nd is a binary format, generic, fast & lighweight
# + PyCloud make it possible to pickle functions dependencies

hmac, hashlib.md5('string').hexdigest()
bz2, gzip, tarfile, zlib.compress(string)
archive = zipfile.ZipFile('foo.zip', mode='w')
for root, dirs, files in os.walk('/path/to/foo'):
    for name in files:
        archive.write(os.path.join(root, name), compress_type=zipfile.ZIP_DEFLATED)

templite, jinja2 # HTML templating system
lxml > HTMLParser (std or html5lib), pyquery, beautifulsoup # use v>=3.2
from lxml import etree
tree = etree.parse(some_file_like_object)
etree.tostring(tree)
root = tree.getroot()
BeautifulSoup('html string').prettify() # newlines+tabs formatted dump

urlparse
requests # replacement for urllib2. Lib to mock it: responses/httmock - Also: aiohttp for asyncio-based equivalent
requests.post('http://urldelamortquitue.com/magicform/', {u'champ1':u"valeur1", u'champ2':u"valeur2"})
HTTPretty # Testing HTTP requests without any server, acting at socket-level

bottle, pyramid, flask # Web frameworks
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

pywebsocket
paramiko # remote SSH/SFTP connexion
boom # like Siege or Funkload : web-app stress testing

mininet # realistic virtual network, running real kernel, switch and application code, on a single machine
ipaddr, netaddr > socket.inet_aton # string IP to 32bits IP + validate IP, !! '192.168' is valid
wifi # wrapper around iwlist and /etc/network/interfaces
tn = telnetlib.Telnet('example.com')
tn.read_until("login: ")
tn.write(user + "\n")

pygeoip, mitsuhiko/python-geoip, python-geoip@code.google,  maxmind/geoip-api-python

deap # genetic programming

EasyDialogs, optparse_gui, EasyGui
pyglet # windowing and multimedia lib
pillow > pil # Python Image Library
AAlib # ASCII rendering

platform # python version, OS / machine / proc info...

ctypes.cdll.LoadLibrary("libc.so.6")
libc = ctypes.CDLL("libc.so.6")
libc.printf("An int %d, a double %f\n", 1234, ctypes.c_double(3.14))

struct # pack/unpack binary formats
binascii.hexkify # display binary has hexadecimal


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
from __future__ import print_function, with_statement, generators...
print('string', file=sys.stderr, end='')

@type_check
def foo(x: between(3, 10), y: is_int) -> is_int:
    return x * y
# Function annotations, see the following SO question that point to PEP 3107 & 0362 (function signatures):
# http://stackoverflow.com/questions/3038033/what-are-good-uses-for-python3s-function-annotations

b'I am an immutable basic byte array of type "bytes"'
bytearray(b"I am mutable")

nonlocal

first, *rest = range(5) # extended iterable unpacking

with concurrent.futures.ProcessPoolExecutor() as executor: # Asynchronous
    processed_args = list(executor.map(big_calculation, args)) # faster than without 'executor'
    futures_url = {executor.submit(other_big_calc, arg) for arg in processed_args}
    for future in as_completed(futures):
        url = futures[future]
        if future.exception():
            raise future.exception()
        yield future.result()

yield from iterator # delegate

def foo(a, b, *, keyword=None): pass # keywords-only functions arguments

class MyClass: pass # no need to inherits from object

class Metaaa(metaclass=MyClass): pass # no more __metaclass__ attribute

super() # new simpler syntax !

obj.__qualname__

from enum import Enum, IntEnum

from functools import singledispatch
