# -*- coding: utf-8 -*-
"""""""""""
"" Tricks
"""""""""""
_ # result of the last expression evaluated (in an interpreter only)

r'''Raw string literal: no need to double escape \{0}\{one:.5f}'''.format("zero", one=1) # raw string: treat backslashes as literal characters
'My name is {0[firstname]} {0[lastname]}'.format({'firstname': 'Jack', 'lastname': 'Vance'})
u"""Unicode string {obj.__class__} {obj!r}""".format(obj=0) # for formatting with a defaultdict, use string.Formatter().vformat
from __future__ import unicode_literals # make all literal strings unicode by default, not ASCII - Gotchas: http://stackoverflow.com/a/827449/636849
unicodedata.normalize('NFKD', u"éçûö") # Also, for Cyrillc, Mandarin... : import unidecode
eyalr/unicode_mayo # detect unicode corruption
chardet.detect(str) # Mozilla encoding detection
str.encode('ascii') # raise a codec exception if the string doesn't only contain ASCII characters - Also: str.decode('utf8')
PYTHONIOENCODING=utf_8 # http://daveagp.wordpress.com/2010/10/26/what-a-character/
with open(file_path, "rb+", buffering=0) as open_file: # open ascii as well as UTF8
    for line in open_file.readlines(): # Drawback: no encoding can be specified
        yield line.rstrip().decode("utf8") # or just open_file.read().decode('utf8')
with io.open('my_file', 'w', encoding='utf-8') as outf: pass # force UTF8 - 'pass' => just 'touch'
for line in fileinput.input([filename], inplace=True):
    print(line.strip())
fileutils.atomic_save # from mahmoud/boltons
intern(str) # internal representation - useful for enums/atoms + cf. http://stackoverflow.com/a/15541556

<module>.__file__ # can refer to .py OR .pyc !!
__all__ = ['bar', 'foo']
# list of symbol to export from module. Default: all symbol not starting with _

__slots__ = ("attr1_name") # flyweight design pattern
# Its proper use is "to save space in objects. Instead of having a dynamic dict that allows adding attributes to objects at anytime, there is a static structure which does not allow additions after creation. This saves the overhead of one dict for every object that uses slots." It also slightly slows down lookup time
# !! Redefining a 'slot' in a child class is UNDEFINED BEHAVIOUR ! cf. https://docs.python.org/2/reference/datamodel.html#__slots__

__unicode__ # return characters
def __str__(self): # return bytes
    return unicode(self).encode('utf-8') # calls __unicode__
__repr__ # unambigous, as possible 'eval'uable
"MyClass(this=%r,that=%r)" % (self.this,self.that)

callable(obj) # == hasattr(obj, '__call__') # both should work for functions too

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

def CtxtMgr(object):
    def __enter__(self): pass
    def __exit__(self, eType, eValue, eTrace): pass
@contextlib.contextmanager
def foobar():
    # __enter__ code
    try:
        yield
    finally:
        # __exit__ code

os.makedirs(dir_path) # + ignore OSError where .errno == errno.EEXIST and os.path.isdir(dir_path) # mkdir -p
tempfile.gettempdir()
tempfile.mkdtemp()
tempfile.NamedTemporaryFile() # file automagically deleted on close()
tempfile.SpooledTemporaryFile(max_size=X) # ditto but file kept in memory as long as size < X

StringIO # fake file
glob, fnmatch # manipulate unix-like file patterns
jaraco/path.py, mikeorr/Unipath # provide a handy 'Path' object (std in Python 3), and a handy walkfiles()
os.stat("filename").st_ino # get inode
.st_size # in bytes. Human readable size: http://stackoverflow.com/q/1094841/636849

watchdog # + cmd watchmedo -> monitor/observe files changes - FROM: S&M

def bar(**kwargs): # != def bar(foo=None, **kwargs):
    foo = kwargs.pop('foo')

arrow, delorean # 'better dates and times' & 'Time Travel Made Easy'
datetime.utcnow() # better than time.time()
import pytz # pytz.utc, pytz.all_timezones
from dateutil import parser # !! ALWAYS pass a Callable as tzinfos so that it won't use the system timezone (time.tzname)
def _tzinfos_pytz_pst_func(tzname, tzoffset):
    tzdata = pytz.timezone('America/Los_Angeles') if tzname == 'PST' else pytz.timezone(tzname)
    if tzoffset:
        tzdata += timedelta(seconds=tzoffset)
    return tzdata
parser.parse(date_string_with_tz, tzinfos=_tzinfos_pytz_pst_func).astimezone(pytz.utc) # !! Won't work for DST ! Else:
pytz.timezone('America/Los_Angeles').localize(parser.parse(date_string_without_tz)).astimezone(pytz.utc)

globals()["Foo"] = Foo = type('Foo', (object,), {'bar':True}) # on-the-fly class creation
module = sys.modules[base_class.__module__].__dict__; module[name] = new.classobj(name, (base_class,), class_attributes) # cleaner Alt
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
@patch("that_context_mgr", MagicMock(__enter__ = lambda *args: MyReturnedObject()))
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

# For a decorator that takes no arg, just get rid of the enclosing function. Deep dive on them at: http://blog.dscpl.com.au/2014/01/implementing-universal-decorator.html
def trace_exec_time(repeat=1, result_strategy=lambda results: results[-1]):
    """
    Valid strategies are: min, max, statistics.mean. Default is to keep only the last result
    """
    def decorator(func):
        @functools.wraps(func)  # TODO: use wrapt.decorator
        def wrapper(*args, **kwargs):
            ret_vals = []
            def exec_func():
                nonlocal ret_vals
                ret_vals.append(func(*args, **kwargs))
            print(func.__name__, args, kwargs, timeit.timeit(exec_func, number=repeat))
            return result_strategy(ret_vals)
        return wrapper
    return decorator
@wrapt.decorator # Proper decorators by Graham Dumpleton - Also: proxy = wrapt.ObjectProxy(original)
def pass_through(wrapped, instance, args, kwargs):
    return wrapped(*args, **kwargs) # 'splat' operator
from tputil import make_proxy # Pypy transparent proxy : can record/intercept/modify operations

# Descriptors
class Property(object):
    def __init__(self, fget):
        self.__doc__ = getattr(fget, '__doc__')
        self.fget = fget

    def __get__(self, obj, type):
        if obj is None:
            return self
        return self.fget(obj)

buffer & memoryview

class Immut2DPoint(namedtuple('_Immut2DPoint', 'x y')):
    __slots__ = () # Else new attributes can still be added to that class dynamically
    def __new__(cls): # Facultative
         return cls.__bases__[0].__new__(cls, 'X', 'Y')
# Cool namedtuple methods: _asdict(), _replace(kwargs), _fields, namedtuple._make(iterable)

# For multiple inheritance with namedtuple, combine fields + use specific inheritance order:
class Immut3DPoint(namedtuple('_Immut3DPoiint', Immut2DPoint._fields + ('z',)), Immut2DPoint):
    __slots__ = ()

LOG_FORMAT = "%(asctime)s - pid:%(process)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s"
def create_logger(): # Also: logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, stream=sys.stderr)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    file_handler = logging.handlers.RotatingFileHandler('proxy.log', maxBytes=1024*1024, backupCount=10) # Also: TimedRotatingFileHandler
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(file_handler)
    return logger
# Lazy logger: http://stackoverflow.com/a/4149231
@deprecated # for legacy code, generates a warning: http://code.activestate.com/recipes/391367-deprecated/ - Alt: OpenStack debtcollector
Twangist/log_calls # logging & func calls profiling
# Support for {} / %(keyword)s format syntaxes:
# - https://docs.python.org/3/howto/logging-cookbook.html#formatting-styles
# - vinay.sajip/logutils/logutils/__init__.py:Formatter - based on http://plumberjack.blogspot.co.uk/2010/10/supporting-alternative-formatting.html
logger = logging.getLogger(__name__)
try: Ellipsis # like 'pass' but as an object, not a statement
except Exception as err: # see chain_errors module
    logger.exception("Additional info: %s", 42) # Exception will be automagically logged
    logging.warn("Hello %(world)r!", world=earth)
    import traceback; error_msg = ''.join(traceback.format_exception(*sys.exc_info())) # Also: tbutils.TracebackInfo from mahmoud/boltons
else: pass
finally: pass

from distutils.command.build import build
class custom_build(build):
    def run(self):
        build.run(self)
        ... # custom init
cmdclass['build'] = custom_build

# Environment variables
export PYTHONSTARTUP="$HOME/.pythonrc" # code to execute when Python starts
PYTHONPATH : directories to add to sys.path # use *.pth files instead for 3rd party modules - See also: import site
PYTHONHOME : Python interpreter directory
PYTHONCASEOK : case insensitive module names (usefule under Windows)
PYTHONIOENCODING : force default encoding for stdin/stdout/stderr
PYTHONHASHSEED : change seed hash() (=> more secure VM)

__main__.py # code executed in case of 'python my_pkg/' or 'python -m my_pkg'
zip -r ../myapp.egg # Make an .egg - You just need a ./__main__.py - See also: zipimport, pkgutil


""""""""""""""""""
"" Data structures
""""""""""""""""""
from bisect import bisect_left # binary/dichotomic search on lists
import heapq # min-heap: .nlargest .nsmallest

collections.deque # double-ended queue, with optional maximum length
queueutils.PriorityQueue # from mahmoud/boltons

collections.Counter([...]).most_common(1) # dict subclass for integer values
unique_id_map = collections.defaultdict(itertools.count().next) # will always return the same unique int when called on an object: unique_id_map['a'] == unique_id_map['a'] != unique_id_map['b']
iterutils.windowed, iterutils.Chunked # iteration from mahmoud/boltons

pyrsistent PVector, PMap, PSet, Precord, PClass, PBag, PList, Pdeque

DanielStutzbach/blist > std list # kind of a rope
pyropes # rope: binary tree-based data structure for efficiently storing and manipulating a very long string
bitarray # array of booleans

Banyan, mozman/bintrees, pytst, rbtree, scipy-spatial # binary, redblack, AVL, ternary-search & k-d trees

marisa-trie, datrie, chartrie, hat-trie, pyjudy, biopython # Tries comparison: http://kmike.ru/python-data-structures/
kmicke/DAWG # Directed Acyclic Word Graphs
ahocorasick, acora # Aho-Corasick automaton : quick multiple-keyword search across text

kayzh/LSHash # locality sensitive hashing

bitly/dablooms, axiak/pybloomfiltermmap, crankycoder/hydra, xmonader/pybloomfilter, TerbiumLabs/pyblume
svpcom/hyperloglog # Super and Hyper Log Log Sketches
jesperborgstrup/Py-IBLT # Invertible Bloom filter - Alt: http://code.activestate.com/recipes/577684-bloom-filter/

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

zip, reduce, all, any, min, max, sum # Cool standard functions to work on lists
# generators expression > list-comprehensions
def stop(): raise StopIteration
list((stop() if e == "BREAK" else e) for e in iterable)
class CustomGenerator(object): # minimal generator protocol
    def __iter__(self):
        yield stuff
        #OR
        return self # then must implement 'next(self)' (__next__ in Python3)
@coroutine # == generator. This decorator is equivalent to a first call to .next()
def printer():
    while True:
        value = (yield 'waiting')
        print(value)
p = printer()
p.next() # returns 'waiting'
p.send('OK') # prints 'OK', returns 'waiting'
p.throw(ValueError, 'Bad value')

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

dict.viewitems() # immutables, not consumable like generators but still very fast

d.setdefault('key', []).append(42) # add element to list, create it if needed
collections.defaultdict # autovivification: def tree(): return defaultdict(tree)

isinstance(obj, collections.Hashable)

collections.OrderedDict # remember insertion order
OrderedDict(sorted(d.iteritems(), key=lambda (k,v): (v,k))) # sort a dict by its values
grantjenks/sorted_containers # faster: SortedList, SortedDict, SortedSet

from itertools import groupby
{category: list(packages) for category, packages in groupby(pkg_list, get_category)} # dict-comprehension, limited: see SO/18664274
{e for e in elems} # set-comprehension

set operators : | & - ^

dict.__missing__ # invoked for missing items

*{'a':0,'b':1}  # ('a', 'b')
assert d == dict(**d)
dict(y, **x) # union of dicts, duplicates are resolved in favor of x

class Bunch(dict): # or inherit from defaultdict - http://code.activestate.com/recipes/52308
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
def Tree(): # fs = Tree(); fs['all']['the']['way']['down']
    return defaultdict(Tree)

ambitioninc/kmatch # a language for filtering, matching, and validating dicts, e.g. K(['>=', 'k', 10]).match({'k':9}) # False
jab/bidict # provide key -> value & value -> key access
dictutils.OrderedMultiDict # from mahmoud/boltons

ultrajson >faster> simplejson >faster> json
def sets_converter(obj): list(obj) if isinstance(obj, set) else obj.__dict__ # or pass custom json.JSONEncoder as the 'cls' argument to 'dumps'
json.dumps(d, sort_keys=True, indent=4, default=sets_converter) # pretty formatting - Alt: pprint.pformat - Also: -mjson.tool

nicolaiarocci/cerberus # validation tool for dictionaries, e.g. type checking
pyrsistent PMap and PREcord  # immutable/functional with invariants and optional types


"""""""""""""""""""
"" Quirks & Gotchas
"""""""""""""""""""
# !! Beware the Method Resolution Order (cls.__mro__) with 'super' : https://fuhm.net/super-harmful

[] = () # is OK, but not: () = []

assert bool(datetime.time(0,0,0)) is False # before 3.5 - cf. "a false midnight" http://lwn.net/Articles/590299/

x = 256
y = 256
assert (x is y) is True
x = 257
y = 257
assert (x is y) is False
x = 257; y = 257
assert (x is y) is True

# DO NOT use other default parameter values than None (or at worst an immutable datastructure), + initialization is static
def foo(x = []):
    x.append('do')
    return x
foo();foo()

tuple(obj) # !! PITFALL: fail for None, will parse any sequence like a basestring and won't work on single value
def to_tuple(t):
    if not t:
        return ()
    elif is_sequence(t):
        return tuple(t)
    else:
        return (t,)

d = {'a':42}
print type(d.keys()[0]) # str
class A(str): pass
a = A('a')
d[a] = 42
print d # {'a':42}
print type(d.keys()[0]) # str

def create_multipliers(n):
    return [lambda x : i * x for i in range(1,n+1)]
for multiplier in create_multipliers(2):
    print multiplier(3) # Late Binding Closure : prints 6 twice

i = 0; a = ['', '']
i, a[i] = 1, 10
print a  # -> ['', 10] - cf. https://news.ycombinator.com/item?id=8091943 - Original blog post from http://jw2013.github.io

issubclass(list, object) # True
issubclass(object, collections.Hashable) # True
issubclass(list, collections.Hashable) # False - There are 1449 such triplets (4.3% of all eligible triplets) in Python 2.7.3 std lib

f = 100 * -0.016462635 / -0.5487545  # observed on the field, in a real-world situation
print '            f:', f              # 3.0
print '       int(f):', int(f)         # 2
print '     floor(f):', floor(f)       # 2.0

# Name mangling:
class Yo(object):
    def __init__(self):
        self.__bitch = True
Yo().__bitch  # AttributeError: 'Yo' object has no attribute '__bitch'
Yo()._Yo__bitch  # True

class O(object): pass
O() == O()             # False
O() is O()             # False
hash(O()) == hash(O()) # True !
id(O()) == id(O())     # True !!!
# ANSWER: http://stackoverflow.com/a/3877275/636849

# The following are taken from cosmologicon Python wats quiz. All assertions are True
'abc'.count('') == 4
1000000 < ''
False == False in [False]

l = ([1],)
l[0] += [2]  # -> raises a TypeError, but l has changed: ([1, 2],)

[4][0.0]   # raises a TypeError
{0:4}[0.0] # evaluates to: 4

[3,2,1] < [1,3]  # False
[1,2,3] < [1,3]  # True


"""""""""""""""""""""""""""
"" Functional Programming
"""""""""""""""""""""""""""
# Guido van Rossum is not a big fan, he wrote the very interesting 'The fate of reduce() in Python 3000'

# Buitins
apply, map, filter, zip # I agree with GvR that a list-comprehension is often clearer than a call to filter
from functools import partial, reduce # for Py3+ compatibility
sum(list_of_lists, []) # flatten a list of lists - Alt: list(itertools.chain.from_iterable(l_o_l)) OR reduce(operator.concat, l_o_l)

# Extra libs
dakerfp/patterns # functional pattern matching through real DSL made by modifying the AST ; http://www.slideshare.net/dakerfp/functional-pattern-matching
toolz # brings: pluck, tail, compose, pipe, memoize - Even faster: CyToolz
suor/funcy
kachayev/fn.py

JulienPalard/Pipe # fib() | where(lambda x: x % 2 == 0) | take_while(lambda x: x < 4000000) | add


"""""""""""""""""
"" Test & Debug
"""""""""""""""""
faulthandler.enable() # dump stacktrace on SIGSEGV, SIGABRT... signals ; python2 -X faulthandler script.py

import faker # generate test data: phone numbers, IPs, URLs, md5 hashes, geo coordinates, user agents, code...
import nose # -m nose.core -v -w dir --pdb --nologcapture --verbose --nocapture /path/to/test_file:TestCase.test_function - Also: http://exogen.github.io/nose-achievements/
nosetest # -vv --collect-only # for debug
py.test -k 'TestClass and test_methode_name' # selective test execution
self.assertRaisesRegexp / assertDictContainsSubset / assertAlmostEqual(expected, measured, places=7)
c-oreills/before_after # provides utilities to help test race conditions
import sure # use assertions like 'foo.when.called_with(42).should.throw(ValueError)'
import doctest # include tests as part of the documentation
AndreaCensi/contracts # Design By Contract lib - Alt: PythonDecoratorLibrary basic pre/postcondition decorator
behave # Behavior Driven Development
brodie/cram # generic command-line app testing
import capsys # capture stdin/out
import monkeypatch # modify an object that will be restored after the unit test
import tmpdir # generate a tmp dir for the time of the unit test
import hypothesis # feed you test with known to break edge cases

module_name=code
code_module_path=$(python -c "import $module_name; print $module_name.__file__" | sed 's/pyc$/py/')
python -mtrace --ignore-module=codeop,__future__ --trace [ $file | $code_module_path ] # trace all code lines run when executing a file / in interactive console
dhellmann/smiley # application tracer, record & report, inspired by rad2py/wiki/QdbRemotePythonDebugger

# IPython tricks
cd /a/path
!cmd # shell command
%quickref
%load script.py # and %%file to write to a file
%save $filename # save session - Alt: %history -> dump it. Stored in ~/.config/ipython/profile_default/history.sqlite - used by pdb too
%pdb # Automatic pdb calling
%timeit do_something()
%debug # post_mortem
%bg # run in the background
%%javascript # and many other languages
from IPython.display import HTML, SVG; HTML(html_string) # render HTML, SVG
ipython notebook # D3 support : wrobstory/sticky
ipython nbconvert --to [html|latex|slides|markdown|rst|python]

# PDB tricks
!p = ... # make it possible to start a cmdline with pdb shorthands
debug foo() # step into a function with pdb
import pdb; foo(42); pdb.pm() # enter debugger post-mortem using:
sys.last_traceback / sys.last_value # non-handled exception info
from IPython.core.debugger import Pdb; Pdb().set_trace()
ipdb.set_trace() / python -mipdb / ipdb.pm() / ipdb.runcall(function, arg)
pdbpp # prettier PDB
google/pyringe # when python itself crashes, gets stuck in some C extension, or you want to inspect data without stopping a program
import rpdb; rpdb.set_trace() # remote debugging
from pdb_clone import pdb; pdb.set_trace_remote() # then pdb-attach : remote-debugging - Also: pdbhandler.register() to enter at any time a running program
boltons.debugutils.pdb_on_signal

from pprint import pprint # indent=4

vars(obj), dir(obj)

inspect.getmembers(obj)
inspect.getargspec(foo_func) # get signature
inspect.getfile(my_module)
inspect.getsource(foo_func) # if implemented in C, use punchagan/cinspect
frame,filename,line_number,function_name,lines,index=inspect.getouterframes(inspect.currentframe())[1]
inspect.currentframe(1).f_locals['foo'] = 'overriding caller local variable!'

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
neuroo/equip # bytecode instrumentation, e.g. insert call counters logic into .pyc
foo.func_code = marshal.loads(marshal.dumps(foo.func_code).replace('bar', 'baz')) # bytecode evil alteration
astor / astunparse # AST 'unparse' : tree -> source

import gc; gc.get_objects() # Returns a list of all objects tracked by the garbage collector
# SUPER powerful to hack python code and sniff values

python -m cProfile myscript.py -o output.pstats # cProfile.Profile().dump_stats(filename)
gprof2dot.py -f pstats output.pstats | dot -Tpng -o output.png
pycallgraph graphviz -- ./mypythonscript.py # Alt for recursion tree: carlsborg/rcviz
kernprof.py --line-by-line myscript.py # line_profiler great pip package
pyprof2calltree # use kcachegrind
python-flamegraph # FlameGraph profiler
https://tech.dropbox.com/2012/07/plop-low-overhead-profiling-for-python/ # like gperftools, sampling profiler for prod servers
http://mg.pov.lt/objgraph # explore Python object graphs
snakefood # draw code base dependency graphs
what-studio/profiling # live profiling
PyVmMonitor # profiler with graphs
objgraph.show_most_common_types() # summary of the number objects (by type) currently in memory

python -mtimeit -s'xs=range(10)' '[hex(x) for x in xs]' # exec time, compare to 'map(hex, xs)'
timeit.timeit(lambda: local_func(), setup="from m import dostuff; dostuff()", number=1000)

# Get memory usage (+ cf. resource below)
from guppy import hpy
h = hpy()
h.heap()
h.iso(...objects...).sp
# Also: http://stackoverflow.com/questions/938733/total-memory-used-by-python-process
asizeof # the simplest solution from: https://pympler.readthedocs.org/en/latest/related.html
rogerhu/gdb-heap
import tracemalloc # Python3

def get_refcount(obj):
    """Valid for CPython implementation only"""
    return ctypes.c_size_t.from_address(id(obj))
# FUN FACT: the references to the 'int' [-5 ; 256] are shared
ctypes.POINTER(c_int).from_address(0)[0] # SEGFAULT
def deref(addr, typ):
    return ctypes.cast(addr, ctypes.POINTER(typ))
deref(id(42), ctypes.c_int)[4] = 100 # change value of 42 ! - '4' is the index to the ob_ival field in a PyIntObject - In Python3 this index is '6'


"""""""""""""""""""""""""
"" Subprocesses & shell
"""""""""""""""""""""""""
# grep-like one-liners:
python -c 'import sys, re; sys.stdout.writelines([str(re.search("REGEX", line).groups())+"\n" for line in sys.stdin])'

from distutils import spawn
cmd_path = spawn.find_executable('cmd') # shutil.which in Python3 / shutilwhich backport else
subprocess.check_output([cmd_path, 'do', 'stuff'], stderr=subprocess.STDOUT, input=bytes(some_text,, 'UTF-8')) # last param added in 3.4 : https://hg.python.org/cpython/file/877f47ca3b79/Lib/subprocess.py#l614
# AVOID PIPE ! Flaws & workarounds: http://www.macaronikazoo.com/?p=607 ; http://eyalarubas.com/python-subproc-nonblock.html

platform # python version, OS / machine / proc info...
resource # limit a process resources: SPU time, heap size, stack size...
print('Memory usage: {} (kb)'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))  # get process memory usage

shlex.split('--f "a b"') # tokenize parameters properly

### sh.py tips & tricks
# Caveat: does not work under Windows
# Alt (but less pythonic/simple IMHO): gawel/chut, plumbum, sarge
# Special keyword args: https://amoffat.github.io/sh/special_arguments.html#special-arguments
- all commands are checked at 'from sh import' time so they are guaranteed to exist
- Always use `_err=sys.stderr` ou `_err_to_out=True` because default is to discard commands stderr
- `print()` is NEEDED to display command output (or you need to use `_out=sys.stdout`)
- `_piped='direct'` is useful to connect processes without consuming any memory
- `_iter` : creates a line generator => you can chain lazy functions taking a 'input_iterator' as input & output
- a command invocation return a `RunningCommand` object, on which you can wait for the text output (by calling `str()` on it)
or get a list of output lines (by calling `list()` on it)

import pip
pip.main(['install', '--proxy=' + PROXY, 'requests==2.7.0', 'retrying==1.3.3', 'sh==1.11'])

import sh, sys
sh = sh(_err=sys.stderr, _out=None)  # setting default commands redirections
sh.bzcat(...)

if len(argv) > 1:
    pipe = cat(argv[1], _iter=True, _err=stderr)  # `pipe` is an input_lines_iterator
else:
    pipe = cat(_in=stdin, _iter=True, _err=stderr)

(import [sh [cat grep wc]]) # in Hy, aka Python with Lisp syntax
(-> (cat "/usr/share/dict/words") (grep "-E" "^hy") (wc "-l"))


""""""""""""""""""""""""""
"" Libs & tools for DEVS !
""""""""""""""""""""""""""
pew > virtualenv # sandbox. To move an existing environment: virtualenv --relocatable $env
pip # NEVER sudo !! > easyinstall - Distutils2 has been abandonned :( Check buildout/conda/bento/hashdist/pyinstaller for new projects or keep using setuptools: https://packaging.python.org
pip --editable $path_or_git_url # Install a project in editable mode (i.e. setuptools "develop mode") from a local project path or a VCS url. FROM: S&M
pip freeze > requirements.txt # dumps all the virtualenv dependencies
pip install --user $USER --src . -r requirements.txt
pip-review # from pip-tools, check for updates of all dependency packages currently installed in your environment : Alt: piprot requirements.txt ; ./manage.py pipchecker
pex # self-contained executable virtual environments : carefully constructed zip files with a #!/usr/bin/env python and special __main__.py - see PEP 441

liftoff/pyminifier # code minifier, obfuscator, and compressor
pyflakes, pylint --generate-rcfile > .pylintrc # static analysis - Also: Flake8, openstack-dev/hacking, landscapeio/prospector, pylama (did not work last tim I tried)
pyreverse # UML diagrams

Cookiecutter # creates projects from project templates, e.g. Django, OpenStack, Kivy... + in other languages !
lobocv/crashreporter #store and send crash reports directly to the devlopers


"""""""""""""""""""""""""""""
"" Libs & tools for SCIENCE !
"""""""""""""""""""""""""""""
nltk, TextBlob # Text analysis : noun phrase extraction, sentiment analysis, translation...
topia.termextract
difflib # compare text/strings/sequences
fuzzywuzzy # fuzzy string comparison ratios, token ratios...
sumy # text summarization - Install: sudo aptitude install libxml2-dev libxslt1-dev && pip install sumy && python -m nltk.downloader -d /usr/share/nltk_data all # 1.7GB
deanmalmgren/textract # extract text from .doc .gif .jpg .oft .pdf .png .pptx .ps ...
snowballstemmer # supports 15 languages

decimal.Decimal # contrary to floats : 3*0.1 - 0.3 == 0.0
float("inf") # infinite !
fractions
statistics # Python 3
kwgoodman/roly # moving window median algorithms - Also: quantile sketches algos in Algo_Notes.md

scipy
    numpy # n-dimensional arrays
    sympy # symbolic mathematics: formula printing (also: PyLatex), simplification, equations, matrices, solvers...
    pandas, sql4pandas # data analysis, to go further : statsmodels, scikit-learn or PyMC (Machine Learning), orange (dedicated soft for visu), miha-stopar/nnets (neural networks)
    matplotlib, prettyplotlib, mpld3, bokeh, vispy # 2d plotting

jhcepas/ete # tree epxloration & visualisation
riccardoscalco/Pykov # markov chains

SimpleCV # powerful computer vision tools : find image edge, keypoints, morphology; can use the Kinect
python-graph-core, networkx, igraph, graph-tool # networks & graphs manipulation

deap # genetic programming
cvxopt # convex optimization

mmap # memory-mapped files
joblib # memoize computations by keeping cache files on disk

rpy2 # acces to R

from cryptography.fernet import Fernet # symmetric encryption
mitsuhiko/itsdangerous # helpers to pass trusted data to untrusted environments by signing content


"""""""""""""""""""""
"" Other libs & tools
"""""""""""""""""""""
reload(module)
modulefinder # determine the set of modules imported by a script

PyPy # can be faster, compiles RPython code down to C, automatically adding in aspects such as garbage collection and a JIT compiler. Also: PyPy-STM
from jitpy.wrapper import jittify # fijal/jitpy : embed PyPy into CPython, can be up to 20x faster
Cython # .pyx : superset of Python with optional static types, can invoke C/C++ and compile down to C
Jython / Py4J # intercommunicate with Java
Numba # NumPy aware dynamic Python compiler using LLVM
Pyston # VM using LLVM JIT
PyInline # put source code from other programming languages (e.g. C) directly "inline" in Python code
Pyrex # write code that mixes Python and C data types and compiles it into a C extension
Nuitka # converts Python code into C++ code (targetting VisualStudio, MinGW or Clang/LLVM compilers)

multiprocessing, Pyro > threading # as Python can only have on thread because of the GIL + using multiprocessing => everything should be pickable
SimPy # Process Interaction
threading.Thread().deamon = True # The entire Python program exits when no alive non-daemon threads are left.
threading.Event # for threads communication, including stopping: Thread.run(self): while not self.stop_event: ...
# Kill a thread ? -> http://stackoverflow.com/a/325528/636849
from multiprocessing.dummy import Pool as ThreadPool # Threads using multiprocessing API
pool = ThreadPool(4); results = pool.map(foo, args); pool.close(); pool.join()

select # efficient I/O
def _make_file_read_nonblocking(f):
    fd = f.fileno()
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
from gevent import monkey; monkey.patch_all() # Greenlets
saucelabs/monocle, Stackless, libevent, libuv, Twisted, Tornado, asyncore # other ASync libs, that is :
# concurrency (code run independently of other code) without parallelism (simultaneous execution of code)
python -m twisted.conch.stdio # Twisted REPL
@asyncio.couroutine # aka Tulip, std in Python 3.3, port for Python 2.7 : trollius
numbapro # for CUDA

autobanh, crossbar.io # WAMP in Python
pywebsocket
xmlrpclib / xmlrpc.client # XML-RPC via HTTP
asynchat, irc, sleekxmpp, embolalia/willie
mailr, mailbox, imaplib, smtpd, smptplib
paramiko # remote SSH/SFTP connexion

celery # distributed task queue - Montoring: mher/flower - Alt: pyres - Also: celery_once to prevent multiple execution and queuing of celery tasks
sched # event scheduler ; Alt: fengsp/plan, crontabber, thieman/dagobah, dbader/schedule, python-crontab, gawel/aiocron, Jenkins, huginn - Also:
luigi, Oozie, Azkaban, Drake, Pinball, Airflow # workflow managers
zeromq, aiozmq, mrq # distributed app / msg passing framework
ampqlib, haigha, puka # AMPQ libs

mrjob, luigi # Hadoop / AWS map-reduce jobs

scales # metrics for Python

pyparsing # create and execute simple grammars instead of regex/lex/yacc - http://pyparsing.wikispaces.com/HowToUsePyparsing

@retry # https://github.com/rholder/retrying - Exponential Backoff algorithm implementation

import uuid # generate unique IDs

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

twobraids/configman > argparse > optparse # Alt: begins > docopt, clize, click - Also: neat quick GUI compatible with argparse: chriskiehl/Gooey
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, fromfile_prefix_chars='@', parents=[parent_parser], conflict_handler='resolve')
parser_group = parser.add_mutually_exclusive_group(required=True)
parser_group.add_argument(... type=argparse.FileType('r'))
return parser.parse_args()
argcomplete # command line tab completion

ConfigParser, configobj # std configuration files format
csvkit > csv, xlwt, xlrd, openpyxl < tablib # generic wrapper around all those. Also: pyxll to write Excel addins & macros in Python
aspy.yaml, yaml # beware the inconsistent behaviours: http://pyyaml.org/ticket/355
cPickle # binary format, generic, fast & lighweight.
# + PyCloud make it possible to pickle functions dependencies

peewee, SQLAlchemy # ORM DB
from playhouse.sqlite_ext import SqliteExtDatabase; db = SqliteExtDatabase(':memory:') # in-memory SQLite DB with peewee
anydbm: dbhash else gdbm else dbm else dumbdbm
sqlite3 # std DB, persistent in a file || can be created in RAM
python-lsm-db(like LevelDB), unqlite-python(like MongoDB), vedis-python(like Redis) # Other embedded NoSQL DBs
pyMySQL, noplay/python-mysql-replication
shelve # other data persistence using pickle, full list of alt: http://docs.python.org/2/library/persistence.html
stephenmcd/hot-redis, getsentry/rb, closeio/redis-hashring

hmac, hashlib.md5('string').hexdigest()
dropbox/python-zxcvbn # password strength estimation
from getpass import getpass # get password without echoing it

lz4, bz2, gzip, tarfile, zlib.compress(string), mitsuhiko/unp # to unpack any archive
archive = zipfile.ZipFile('foo.zip', mode='w')
for root, dirs, files in os.walk('/path/to/foo'): # path.py walkfiles() is even better to crawl a directory tree / files hierarchy - And benhoyt/scandir is faster and now in the Python 3.5 stdlib
    for name in files:
        archive.write(os.path.join(root, name), compress_type=zipfile.ZIP_DEFLATED)

templite, wheezy.template, mako, jinja2 # HTML template system - Note: {{"{{"}} escapes {{
hickford/MechanicalSoup
lxml > HTMLParser (std or html5lib), pyquery, beautifulsoup # use v>=3.2
import lxml.etree, lxml.html
html_root = lxml.html.fromstring('html string') # Alt: html_tree.getroot()
html_tree = lxml.etree.ElementTree(html_root) # Alt: lxml.etree.parse(some_file_like_object)
html_tree.getpath(element)
element.getparent().remove(element)
BeautifulSoup('html string').prettify() # newlines+tabs formatted dump - Alt, less pretty: lxml.html.tostring(element) / lxml.etree.tostring

urlparse.urljoin, urllib.quote_plus # urlencoding & space -> +
requests.post(form_url, data={'x':'42'}) # replacement for urllib2. Lib to mock it: responses/httmock - Also:
    aiohttp # for asyncio-based equivalent
    requests-futures # for asynchronous (non-blocking) HTTP requests
    txrequests # Twistted asynchronous requests
    requests-cache
requests.get(url, headers={"Client-IP":ip, "User-Agent": ua}, allow_redirects=true, stream=True)
status_string = requests.status_codes._codes[404][0]; status_string = ' '.join(w.capitalize() for w in status_string.split('_')) # Alt: httplib.responses, cf. HTTP_STATUS_LINES in Bottle code: http://bottlepy.org/docs/dev/bottle.py
wget # equivalent lib to the command-line tool
HTTPretty # Testing HTTP requests without any server, acting at socket-level
kevin1024/vcrpy # record / replay HTTP interactions

# Web frameworks (from barcamp@AFPY):
bottle # include server, only 1 file long, behind 0bin
CherryPy # good prod server, very easy to launch
flask # good for simple APIs - Alt: hug, based on Falcon, which provides auto documentation, input validation, type-handling with annotations and automatic versions
Django # template engine 0/20 (should be replaceable soon) / ORM++, as good as SQLAlchemy but more high-level
pyramid # more modular alternative to Django
+ web.py
python -m SimpleHTTPServer 8080 # --version > 3: -m http.server
# Basic request parsing:
import re, SimpleHTTPServer, SocketServer
class JsonHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        request_match = re.search('param1=([^&]+)', self.path)
        if request_match:
            self.path = param1_match.group(1) + '.json'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
SocketServer.TCPServer(('localhost', 8080), JsonHandler).serve_forever()
# Flask tricks:
app.logger.addHandler(file_handler)
@app.errorhandler(404) # or 500
def internal_error(exception):
    app.logger.exception("Error 404: %r", {k:getattr(exception, k) for k in dir(exception)})
    raise_chained(exception, 'Error 500: ')
# Also, catch-all URL: http://flask.pocoo.org/snippets/57/

make html # Pelican static HTML files generation, using Jinja2 templates
make serve # preview Pelican articles in localhost, with optional autoreload on edit
sitemap, extract-toc, Tipue-search # plugins

locust # load testing simulating millions of simultaneous users
mininet # realistic virtual network, running real kernel, switch and application code, on a single machine
ipaddr, netaddr > socket.inet_aton # string IP to 32bits IP + validate IP, !! '192.168' is valid
scapy # packet injection/manipulation for many network protocols
wifi # wrapper around iwlist and /etc/network/interfaces
webbrowser.open_new_tab # Firefox/Opera/Chrome instrumentation
tn = telnetlib.Telnet('example.com')
tn.read_until("login: ")
tn.write(user + "\n")

pygeoip, mitsuhiko/python-geoip, python-geoip@code.google, maxmind/geoip-api-python, pierrrrrrre/PyGeoIpMap # this latest one provide a useful command-line tool
OpenTransitTools/gtfsdb # GTFS (General Transit Feed Specification) DB : public transportation schedules and associated geographic information

pygst # GStreamer : media-processing framework : audio & video playback, recording, streaming and editing
jiaaro/pydub # manipulate audio with a simple and easy high level interface (with ugly operator override)

pyglet # windowing and multimedia lib
pysoy # 3D game engine
Zulko/gizeh, Zulko/MoviePy, jdf/processing.py # Video & image (including GIFs) editing
cairo # graphics library outputting .ps .pdf .svg & more
wand (ImageMagick binding), pillow > pil # Python Image Library
ufoym/cropman # face-aware image cropping
andersbll/neural_artistic_style # transfer the style of one image to the subject of another image
lincolnloop/python-qrcode > pyqrcode # use PIL > C++ & Java
AAlib # ASCII rendering
fogleman/Tiling # pavages
graphviz # graphs generation and export as images
pyexiv2 # images EXIF manipulation
antiboredom/audiogrep

EasyDialogs, optparse_gui, EasyGui > Tkinter

fmoo/python-editor # programmatically open a text editor, captures the result
urwid # console user interface lib - Alt: snack, NPyScreen
code.InteractiveConsole().interact() # interactive python prompt
pyreadline, readline, rlcompleter
termcolor, colorama # cross-platform colored terminal text
tqdm # KISS progress bar
PrettyTable # pretty ASCII tables output
bashplotlib # terminal plotting of histograms / scatterplots from list of coordinates

ctypes.cdll.LoadLibrary("libc.so.6")
libc = ctypes.CDLL("libc.so.6")
libc.printf("An int %d, a double %f\n", 1234, ctypes.c_double(3.14))

cffi # C Foreign Function Interface for Python : call compiled C code from interface declarations written in C

struct # pack/unpack binary formats
binascii.hexkify # display binary has hexadecimal


""""""""
"" Django
""""""""
django-admin.py startproject demelons_django
./manage.py syncdb
./manage.py migrate # v1.7 migrations, previously handled by e.g. South
# Also: makemigrations -> create new migrations based on the changes you have made to your models ; sqlmigrate -> displays the SQL statements for a migration
./manage.py runserver
./manage.py startapp profiles
./manage.py dumpdata auth.User --indent 4
./manage.py testserver fixtures/initial_data.yaml
./manage.py test animals.tests.AnimalTestCase.test_animals_can_speak # --pattern="tests_*.py" # --keepdb
./manage.py loaddata fixtures/initial_data.yaml
djshell --settings=debug # use IPython shell from django-extensions

pip install pyparsing==1.5.7 && pip install pydot && ./manage.py graph_models -a -g -o pretty_models_visualization.png

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

AppConfig.ready() # to perform initialization tasks (such as registering signals); called as soon as the registry is fully populated; !! AVOID INTERACTING WITH THE DB !! -> use migrations and e.g. RunPython to populate the DB with initial data

djangocolors_formatter.py # one-file recipe
django-debug-toolbar
django-toolbelt
stripe # payments app
Tastypie # webservice framework to creating REST-style APIs, e.g. for an autocompletion service
factoryboy # > fixtures for DB testing (personnal opinion: several fixtures can sometimes be simpler AND avoid dangerous over-mocking)

all_users_cache = list(User.objects.all()) # force QuerySet evaluation => DB query
.save() / .bulk_create() / .objects.update_or_create()

from django import template
register = template.Library()
@register.filter(is_safe=True)
def hasattribute(obj, attr_name):
    return hasattr(obj, attr_name)

# debug.py - USAGE: ./manage.py runserver --settings=debug
from demelons_django.settings import *
DEBUG = True
TEMPLATE_DEBUG = True
class InvalidVarException(object):
    ...
TEMPLATE_STRING_IF_INVALID = InvalidVarException()

<pre> {% filter force_escape %} {% debug %} {% endfilter %} </pre>


""""""""
"" Fun
""""""""
# Funny loop construct (exist also: try/except/else)
for ...:
    break
else:

from __future__ import braces

import this
import antigravity

a='a=%s;print a%%`a`';print a%`a` # Quine


"""""""""""
" Python 3
"""""""""""
sys.version_info[0] >= 3

from __future__ import division, print_function
print('string', file=sys.stderr, end='')

from typecheck import typecheck, dict_of # prechelt/typecheck-decorator
@typecheck
def foo(x: between(3, 10), y: is_int) -> is_int:
    return x * y
# Function annotations, see the following SO question that point to PEP 3107 & 0362 (function signatures):
# http://stackoverflow.com/questions/3038033/what-are-good-uses-for-python3s-function-annotations
http://code.activestate.com/recipes/426123/ # Port to Python 2.7
mypy # Alt static type checker: py -3.4 -m pip install --user mypy-lang; mypy $script.py

b'I am an immutable basic byte array of type "bytes"'
bytearray(b"I am mutable")

__bytes__() and __str__()

nonlocal

first, *rest, last = range(5) # extended iterable unpacking

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

from functools import \
        singledispatch, \ @foo.register(int) def _(obj, verbose=False): ...
    total_ordering, # to define all comparison methods given __eq__ and __lt__, __le__, __gt__, or __ge__
    lru_cache # memoize / cache for pure functions ; Alt: Py2.7 decorator recipe for caching with TTL : https://wiki.python.org/moin/PythonDecoratorLibrary#Cached_Properties ; or: pypi/cached-property ; or boltons.cacheutils.LRI / boltons.cacheutils.LRU

collections.ChainMap # view of multiple dicts - Hidden Py2.7 backport: from ConfigParser import _Chainmap as ChainMap - Alt: Py2ChainMap

"""""""""""
" Python 3.5
"""""""""""
# PEP448 : unpacking generalized
l = (1, *[2])
d = {"j": 9, **{"i": 8}}

async def foo(): ...

python -m zipapp my_project_dir  # generates a .pyz
