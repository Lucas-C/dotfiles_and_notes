# To list this file sections: $ grep '^"" ' notes.py

"""""""""""""
"" Why Python ?
"""""""""""""
- extremely readable (cf. zen of Python + [this 2013 study](http://redmonk.com/dberkholz/2013/03/25/programming-languages-ranked-by-expressiveness/))
- simple & fast to write
- very popular (taught in many universities)
- has an extremely active development community
- there’s a library for everything: `import antigravity`
- play nicely with other languages
- usable in many fields: scripting & automation, web, network packets manipulation, maths & big data, images & videos manipulation
- many world class companies use it: Google, Facebook, Instagram, Spotify, Quora, Netflix, Dropbox, Reddit
cf. https://realpython.com/world-class-companies-using-python/
It is one of the 3 official Google languages, with C++, Go & - BUT:
> We found out how 20 developpers ran circle around our hundreds of great developpers.
> The solution was very simple ! Those 20 guys were using Python.
FROM: Alex Martelli, in "Python Interviews: Discussions with Python Experts", on Youtube vs Google Video (C++)


"""""""
"" Misc
"""""""
_ # result of the last expression evaluated (in an interactive interpreter)

os.chdir(os.path.dirname(os.path.realpath(__file__))) # useful at beginning of a script : change the current directory to the script parent directory - Alt: Path(__file__).resolve().parent
<module>.__file__ # can refer to .py OR .pyc !!
__all__ = ['bar', 'foo']  # list of symbol to export from module. Default: all symbol not starting with _

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

globals()["Foo"] = Foo = type('Foo', (object,), {'bar':True}) # on-the-fly class creation
module = sys.modules[base_class.__module__].__dict__; module[name] = new.classobj(name, (base_class,), class_attributes) # cleaner Alt
# !!WARNING!! `type()` uses the current global __name__ as the __module__, unless it calls a metaclass constructor
# -> http://stackoverflow.com/questions/14198979/python-inheritance-metaclasses-and-type-function

# `type` is the metaclass Python uses to create all classes behind the scenes
# aka, the most common __class__.__class__ of an object
# But you can specify your own __metaclass__ !

def incr(i):
    incr.counter += i
    return incr.counter
incr.counter = 0 # Function attribute
obj.method = types.MethodType(function, obj) # binding functions into methods

# For a decorator that takes no arg, just get rid of the enclosing function. Deep dive on them at: http://blog.dscpl.com.au/2014/01/implementing-universal-decorator.html
def trace_exec_time(repeat=1, result_strategy=lambda results: results[-1]):
    "Valid strategies are: min, max, statistics.mean. Default is to keep only the last result"
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

# Environment variables
export PYTHONSTARTUP="$HOME/.pythonrc" # code to execute when Python starts
PYTHONPATH : directories to add to sys.path # see also: import site - use *.pth files instead for 3rd party modules, ex: echo ~/anaconda/env3.5/lib/python3.5/site-packages > $VIRTUAL_ENV/lib/python3.5/site-packages/extra_paths.pth
PYTHONHOME : Python interpreter directory
PYTHONCASEOK : case insensitive module names (useful under Windows)
PYTHONIOENCODING : force default encoding for stdin/stdout/stderr
PYTHONHASHSEED : change seed hash() (=> more secure VM)
PYTHONINSPECT : enter interactive mode after executing the script or the command
PYTHONUNBUFFERED=1  # required to flush logs in docker-compose -> https://github.com/docker/compose/issues/4837#issuecomment-302765592

sys.meta_path  # a list of *finder* objects that have their find_module() methods called to see if one of the objects can find the module to be imported - cf. PEP 302

__main__.py # code executed in case of 'python my_pkg/' or 'python -m my_pkg'


"""""""""""""""""""""""""""""""
"" Files, strings & encoding
"""""""""""""""""""""""""""""""
intern(str) # internal representation - useful for enums/atoms + cf. http://stackoverflow.com/a/15541556

PYTHONIOENCODING=utf_8 # http://daveagp.wordpress.com/2010/10/26/what-a-character/
PYTHONUTF8 # cf. https://www.python.org/dev/peps/pep-0540/

r'Raw string literal: no need to double escape \{0}\{one:.5f}'.format("zero", one=1) # raw string: treat backslashes as literal characters
'My name is {0[firstname]} {0[lastname]}'.format({'firstname': 'Jack', 'lastname': 'Vance'})
u"Unicode string {obj.__class__} {obj!r}".format(obj=0) # for formatting with a defaultdict, use string.Formatter().vformat
"\N{Sauropod}" * 10 # you can insert Emoji using `\N{NAME_OF_EMOJI}`
from __future__ import unicode_literals # make all literal strings unicode by default, not ASCII - Gotchas: http://stackoverflow.com/a/827449/636849
unicodedata.normalize('NFKD', u"éçûö") # Also, for Cyrillc, Mandarin... : import unidecode
eyalr/unicode_mayo # detect unicode corruption
chardet.detect(str) # Mozilla encoding detection
str.encode('ascii') # raise a codec exception if the string doesn't only contain ASCII characters - Also: str.decode('utf8')
with open(file_path, "rb+", buffering=0) as open_file: # open ascii as well as UTF8
    for line in open_file.readlines(): # Drawback: no encoding can be specified
        yield line.rstrip().decode("utf8") # or just open_file.read().decode('utf8')

with io.open('my_file', 'w', encoding='utf-8') as outf: pass # force UTF8 - 'pass' => just 'touch'

try:
    for line in fileinput.input([filename], inplace=True, backup='.bak'):
        print(line.strip())
except Exception as error:  # e.g. for UnicodeDecodeError
    os.remove(filename)  # needed on Windows apparently
    os.replace(filename + '.bak', filename)
    raise

def find_usage(string):  # simili-grep
    for dirpath, dnames, fnames in os.walk(STATICS_SRC_DIR):
        for file_name in [os.path.join(dirpath, f) for f in fnames if any(f.endswith(ext) for ext in TARGET_FILES_EXTENSIONS)]:  # compatible Python 2 & 3
            with io.open(file_name, 'r', encoding='utf-8') as open_file:  # compatible Python 2 & 3
                for line_number, line in enumerate(open_file.readlines(), 1):
                    if string in line:
                        yield line, line_number

pattern = (
"^"         # beginning of string
"(?P<word>" # named group start
r"\b\w+\b"  # a word between two word separators
"\.*?"      # non greedy wildcard
")"         # named group end
) # Alt: re.VERBOSE / re.X
m = re.search(pattern, "Un... Deux... Trois...", re.DOTALL|re.MULTILINE) # re.DEBUG -> print parse tree
m.group('word')
# You can also call a function every time something matches a regular expression
re.sub('a|b|c', rep_func, string) # def rep_func(matchobj): ... - More powerful than str.replace for substitutions - Alt, more efficient lib: flashtext
'A B\tC\n'.translate({ord('\t'): ' ', ord('\n'): ''})  # multi-replace
eriknyquist/librxvm # non-backtracking NFA-based regular expression library, for C and Python - Alt: xysun/regex
pyparsing # create and execute simple grammars instead of regex/lex/yacc - http://pyparsing.wikispaces.com/HowToUsePyparsing - Also: parsimonious (used at eBay) & parsley for EBNF & erezsh/lark for LALR - cf. https://tomassetti.me/parsing-in-python/ & lark-parser/lark for Earley & LALR(1)
pycparser # C language code parser
parso # a Python parser

os.makedirs(dir_path) # + ignore OSError where .errno == errno.EEXIST and os.path.isdir(dir_path) # mkdir -p
tempfile.gettempdir()
tempfile.mkdtemp()
tempfile.NamedTemporaryFile() # file automagically deleted on close() - DO NOT USE if project must be Windows-compatible : http://stackoverflow.com/a/23212515/636849 - Also got bad surprises when used in a Github Actions pipeline (probably Docker): https://github.com/PyFPDF/fpdf2/pull/33
tempfile.SpooledTemporaryFile(max_size=X) # ditto but file kept in memory as long as size < X

StringIO # fake file from string - in module StringIO in Python 2, in io in Python 3

glob, fnmatch # manipulate unix-like file patterns
jaraco/path.py, mikeorr/Unipath # provide a handy 'Path' object (std in Python 3 as pathlib), and a handy walkfiles()

os.stat("filename").st_ino # get inode
.st_size # in bytes. Human readable size: http://stackoverflow.com/q/1094841/636849

fileutils.atomic_save # from mahmoud/boltons
portalocker # easy API to file locking

mmap # memory-mapped files - Also: smmap


"""""""""""""""""""
"" Dates & time
"""""""""""""""""""
arrow, delorean # 'better dates and times' & 'Time Travel Made Easy'
freach/udatetime # Fast RFC3339 compliant Python date-time library, timezone aware, with strict format
datetime.utcnow() # better than time.time()
import pytz # pytz.utc, pytz.all_timezones
from dateutil import parser # !! ALWAYS pass a Callable as tzinfos so that it won't use the system timezone (time.tzname)
def _tzinfos_pytz_pst_func(tzname, tzoffset):
    tzdata = pytz.timezone('America/Los_Angeles') if tzname == 'PST' else pytz.timezone(tzname)
    if tzoffset:
        tzdata += timedelta(seconds=tzoffset)
    return tzdata
parser.parse(date_string_with_tz, tzinfos=_tzinfos_pytz_pst_func).astimezone(pytz.utc) # !! Won't work for DST ! "Unfortunately using the tzinfo argument of the standard datetime constructors ‘’does not work’’ with pytz for many timezones."-> Alt:
pytz.timezone('America/Los_Angeles').localize(parser.parse(date_string_without_tz)).astimezone(pytz.utc)
radicale # CalDAV (calendar) and CardDAV (contact) server


"""""""""""""""""""
"" Logging & exceptions
"""""""""""""""""""
if args.debug:
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, # default stream, but explicit beats implicit
        format="%(asctime)s - pid:%(process)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s")
        # all availables format fields: thread, module, name, funcName... https://docs.python.org/3/library/logging.html#logrecord-attributes
else:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(message)s")
def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    file_handler = logging.handlers.RotatingFileHandler('proxy.log', maxBytes=1024*1024, backupCount=10) # Also: TimedRotatingFileHandler
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(file_handler)
    return logger
# Lazy logger: http://stackoverflow.com/a/4149231
@deprecated # for legacy code, generates a warning: http://code.activestate.com/recipes/391367-deprecated/ - Alt: OpenStack debtcollector or even better briancurtin/deprecation or manually: warnings.warn(message, DeprecationWarning, stacklevel=2)
Twangist/log_calls # logging & func calls profiling with a decorator
ScatterHQ/eliot # logging system for complex & distributed systems that outputs causal chains of actions happening within and across process boundaries - `Based on contexts: with start_action(...):`
prezi/python-zipkin # -> dead project ? + no support for Python 3 : https://github.com/prezi/python-zipkin/issues/8
string.Template # $-based substitutions
# Support for {} / %(keyword)s format syntaxes:
# - https://docs.python.org/3/howto/logging-cookbook.html#formatting-styles
# - vinay.sajip/logutils/logutils/__init__.py:Formatter - based on http://plumberjack.blogspot.co.uk/2010/10/supporting-alternative-formatting.html
logger = logging.getLogger(__name__)

# Capturing / detecting a specific log:
from logging.handlers import BufferingHandler
log_handler = BufferingHandler(capacity=100)
logger.addHandler(log_handler)
...  # call code that generates logs
print(log_handler.buffer)  # list of LogRecord

from logging_tree import printout  # from logging_tree package
printout()  # print out the details of the current logging configuration.

import exceptions # contains the list of all std ones
try: Ellipsis # like 'pass' but as an object, not a statement
except Exception as err: # see chain_errors module
    logger.exception("Additional info: %s", 42) # Exception will be automagically logged
    logging.warn("Hello %(world)r!", world=earth)
    import traceback; error_msg = traceback.format_exc() # Also: tbutils.TracebackInfo from mahmoud/boltons
else: pass
finally: pass

from returns.result import Result, Success, Failure  # "Make your functions return something meaningful, typed, and safe" - Railway Oriented Programming - cf. https://sobolevn.me/2019/02/python-exceptions-considered-an-antipattern

Delgan/loguru # Features: values of variables, color, rotation / retention / compression, can be structured as JSON, asynchronous / thread-safe / multiprocess-safe


"""""""""""""""""""
"" Data structures
"""""""""""""""""""
from bisect import bisect_left # binary/dichotomic search on lists
import heapq # priority queue / min-heap: .nlargest .nsmallest - cf. projecteuler/problem081.py

collections.deque # double-ended queue, with optional maximum length
queueutils.PriorityQueue # from mahmoud/boltons
from queuelib import FifoDiskQueue # disk-persisted FIFO queue

collections.Counter([...]).most_common(1) # dict subclass for integer values
unique_id_map = collections.defaultdict(itertools.count().next) # will always return the same unique int when called on an object: unique_id_map['a'] == unique_id_map['a'] != unique_id_map['b']
iterutils.windowed, iterutils.Chunked # iteration from mahmoud/boltons

pyrsistent PVector, PMap, PSet, Precord, PClass, PBag, PList, Pdeque

DanielStutzbach/blist > std list # kind of a rope
pyropes # rope: binary tree-based data structure for efficiently storing and manipulating a very long string
pytries
    marisa-trie  # static memory-efficient Trie-like structures based on marisa-trie C++ library
    datrie  # fast, efficiently stored Trie for Python. Uses libdatrie
    hat-trie  # wrapper for hat-trie C library, an extremely efficient (space and time) modern variant of tries
    DAWG  # DAFSA-based dictionary-like read-only objects. Based on `dawgdic` C++ library - Alt: DAWG-Python in pure Python
bitarray # array of booleans

Banyan, mozman/bintrees, pytst, rbtree, scipy-spatial # binary, redblack, AVL, ternary-search & k-d trees
conceptsandtraining/libtree # deal with large, hierarchical data sets. Runs on top of PostgreSQL

marisa-trie, datrie, chartrie, hat-trie, pyjudy, biopython # Tries comparison: http://kmike.ru/python-data-structures/
kmicke/DAWG # Directed Acyclic Word Graphs
JaredMHall/reline # CLI tool to reformat a text into a specified number of words per line/characters per line

kayzh/LSHash # locality sensitive hashing
JohannesBuchner/imagehash  # perceptual hashes lib, supports: average hashing (aHash), perception hashing (pHash), difference hashing (dHash), wavelet hashing, like pHash but uses DWT instead of DCT (wHash)
zacharyvoase/humanhash # humanize(digest) == 'three-georgia-xray-jig'
pavlovml/match # Scalable reverse image search built on Kubernetes and Elasticsearch

bitly/dablooms, axiak/pybloomfiltermmap, crankycoder/hydra, xmonader/pybloomfilter, TerbiumLabs/pyblume, jaybaird/python-bloomfilter
svpcom/hyperloglog # Super and Hyper Log Log Sketches
jesperborgstrup/Py-IBLT # Invertible Bloom filter - Alt: http://code.activestate.com/recipes/577684-bloom-filter/

immutables.Map # high-perf & memory-efficient immutable mappings implemented using Hash Array Mapped Trie (HAMT) - Better than std types.MappingProxyType because it is hashable - cf. also @dataclass

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
@coroutine # == asyncio generator. This decorator is equivalent to a first call to .next()
def printer():
    while True:
        value = yield 'waiting'
        print(value)
p = printer()
next(p) # returns 'waiting'
next(p) # prints 'None', returns 'waiting'
p.send('OK') # prints 'OK', returns 'waiting'
p.throw(ValueError, 'Bad value')

generator_bit = 1 << 5
bool(gen_fn.__code__.co_flags & generator_bit) # check if a function is a generator

# Is a dict / list ? -> http://docs.python.org/2/library/collections.html#collections-abstract-base-classes
# isinstance(d, collections.Mapping) won't work if the class is not registered, so better check:
hasattr(d, '__getitem__') and hasattr(d, 'keys')

for index, item in enumerate(iterable): ...

# Loop & modify transparently standard DS
items = zip(xrange(0, len(ds)), ds) # lists, tuples & namedtuples
items = d.iteritems() # dicts ( iteritems > items )

buffer & memoryview # cf. https://julien.danjou.info/high-performance-in-python-with-zero-copy-and-the-buffer-protocol/

from tputil import make_proxy # record/intercept/modify operations on list, from Pypi code, deprecated

# Descriptors
class Property(object):
    def __init__(self, fget):
        self.__doc__ = getattr(fget, '__doc__')
        self.fget = fget

    def __get__(self, obj, type):
        if obj is None:
            return self
        return self.fget(obj)

class Immut2DPoint(namedtuple('_Immut2DPoint', 'x y')):
    __slots__ = () # Else new attributes can still be added to that class dynamically
    def __new__(cls): # Facultative
         return cls.__bases__[0].__new__(cls, 'X', 'Y')
# Cool namedtuple methods: _asdict(), _replace(kwargs), _fields, namedtuple._make(iterable)
# For multiple inheritance with namedtuple, combine fields + use specific inheritance order:
class Immut3DPoint(namedtuple('_Immut3DPoint', Immut2DPoint._fields + ('z',)), Immut2DPoint):
    __slots__ = ()
# BUT seriously, use the "attrs" library instead: https://glyph.twistedmatrix.com/2016/08/attrs.html
class Point(typing.NamedTuple):  # https://github.com/topper-123/Articles/blob/master/New-interesting-data-types-in-Python3.rst
    x: int
    y: int
# or traitlets if you need to react when properties values change: https://traitlets.readthedocs.io/en/stable/using_traitlets.html

@pikepdf._methods.augments # Attach methods of a support class to an existing class


"""""""""""""
"" dict & set
"""""""""""""
# Extremely fast as long as < one million elems

dict.viewitems() # immutables, not consumable like generators but still very fast

d.setdefault('key', []).append(42) # add element to list, create it if needed
collections.defaultdict # autovivification: def tree(): return defaultdict(tree)

isinstance(obj, collections.Hashable)

list.sort() is slightly faster & memory efficient than sorted(list)
collections.OrderedDict # remember insertion order
OrderedDict(sorted(d.iteritems(), key=lambda e: e[1])) # sort a dict by its values
grantjenks/sorted_containers # faster: SortedList, SortedDict, SortedSet

from itertools import groupby
{category: list(packages) for category, packages in groupby(pkg_list, get_category)} # dict-comprehension, limited: see SO/18664274
{e for e in elems} # set-comprehension

set operators : | & - ^

dict.__missing__ # invoked for missing items

*{'a':0,'b':1}  # ('a', 'b')
assert d == dict(**d)  # !!WARNING!! only works if `d` keys are strings
dict(y, **x) # union of dicts, duplicates are resolved in favor of x !!WARNING!! only works if `d` keys are strings - Prefer the following in 3.5+ : {**defaults, **user}

class Bunch(dict): # or inherit from defaultdict - http://code.activestate.com/recipes/52308 - or simply use types.SimpleNamespace or argparse.Namespace
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
def Tree(): # fs = Tree(); fs['all']['the']['way']['down']
    return defaultdict(Tree)

keleshev/schema # validating Python data structures, such as those obtained from config-files, forms, external services or command-line parsing, converted from JSON/YAML (or something else) to Python data-types
ambitioninc/kmatch # a language for filtering, matching, and validating dicts, e.g. K(['>=', 'k', 10]).match({'k':9}) # False
nicolaiarocci/cerberus # validation tool for dictionaries, e.g. type checking
pyrsistent PMap and PREcord  # immutable/functional with invariants and optional types
jab/bidict # provide key -> value & value -> key access
dictutils.OrderedMultiDict # from mahmoud/boltons

ijson  # battle-tested, fantastically more memory-efficient
ultrajson >faster> simplejson >faster>(not in my experience on CSC in Py3) json  # Also: rapidjson - ijl/orjson - mitghi/cyjson - Note for ultrajson: it can fail silently: https://github.com/esnme/ultrajson/issues/134 - Good read: https://blog.ionelmc.ro/2015/11/22/memory-use-and-speed-of-json-parsers/
def sets_converter(obj): return list(obj) if isinstance(obj, set) else obj.__dict__ # or pass custom json.JSONEncoder as the 'cls' argument to 'dumps'
json.dumps(d, sort_keys=True, indent=4, default=sets_converter) # pretty formatting - Alt: pprint.pformat - Also: -mjson.tool
for error in jsonschema.Draft4Validator(schema).iter_errors(data): # Alt: kwalify - YAML/JSON validation library based on a schema
    print('#/' + '/'.join(map(str, error.path)), error.message)
jsondiff
jmespath # query language for JSON, ex: foo.*.bar[*].name[-1]


"""""""""""""""""""
"" Quirks & Gotchas
"""""""""""""""""""
# !! Beware the Method Resolution Order (cls.__mro__) with 'super' : https://fuhm.net/super-harmful

float('-iNf') # infinite ! Also: float('nan')

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
foo();foo()  # cf. foo.__defaults__

tuple(obj) # !! PITFALL: fail for None, will parse any sequence like a basestring and won't work on single value
def to_tuple(t):
    if not t:
        return ()
    elif isinstance(t, collections.Iterable):
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
    print multiplier(3) # Late Binding Closure : prints 6 twice - Same can append with 'def' functions

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

a = 1234.567; b = 45.67834; c = 0.0004
(a+b)+c != a+(b+c)  # From: https://en.wikipedia.org/wiki/Floating-point_arithmetic#Accuracy_problems

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
1000000 < '' and () > []  # "objects of different types except numbers are ordered by their type names"
False == False in [False]

l = ([1],)
l[0] += [2]  # -> raises a TypeError, but l has changed: ([1, 2],)

[4][0.0]   # raises a TypeError
{0:4}[0.0] # evaluates to: 4

[3,2,1] < [1,3]  # False
[1,2,3] < [1,3]  # True

x, y = (0, 1) if True else None, None # -> ((0, 1), None)
x, y = (0, 1) if True else (None, None) # -> (0, 1)

class AutoIntEnum(enum.IntEnum):  # recipe from https://docs.python.org/3/library/enum.html#autonumber
    def __new__(cls):
        value = len(cls.__members__)
        obj = int.__new__(cls)
        obj._value_ = value
        return obj
class CrazyEnum(AutoIntEnum):
    A = ()
    B = ()
CrazyEnum.A == CrazyEnum.B # True

json.loads('[NaN]') # [nan]
json.loads('[-Infinity]') # [-inf]

1 if 1 else 0 + 1 if 1 else 0

'a' in 'aa' in 'aaa'

int('١٢٣٤٥٦٧٨٩') # 123456789 - cf. http://chris.improbable.org/2014/8/25/adventures-in-unicode-digits/

# The following gotchas come from https://github.com/satwikkansal/wtfpython
d = {1.0: 'JavaScript'}
d[True] = 'Python'
len(d) == 1 # that's because 1.0 == True aka hash(1.0) == hash(True) (but: 1.0 is not True)

array = [1, 8, 15]
g = (x for x in array if array.count(x) > 0)
array = [2, 8, 22]
list(g) == [8] # in a generator expression, the in clause is evaluated at declaration time, but the conditional clause is evaluated at run time

x = {0: None}
for i in x:
    del x[i]
    x[i+1] = None
    print(i)
# runs for exactly eight times and stops => iteration over a dictionary that you edit at the same time is not supported
# it runs eight times because that's the point at which the dictionary resizes to hold more keys (implementation detail)

r'\OK'
r'\FAIL\' # SyntaxError: EOL while scanning string literal

a, b = a[b] = {}, 5 # a is now: {5: ({...}, 5)}

'a'[0][0][0][0][0]

False == False in [False]   # True
(False == False) in [False] # False
False == (False in [False]) # False

defaultdict(int)['foo']      # 0
defaultdict(int).get('foo')  # None

e = 2.718
try:
    1/0
except ZeroDivisionError as e:
    pass
print(e)  # raise a NameError - cf. https://pydist.com/blog/python-except

d = {}
sys.getsizeof(d)  # 240
d.clear()
sys.getsizeof(d)  # 72 - cf. https://lerner.co.il/2019/05/12/python-dicts-and-memory-usage/

f = open('/tmp/a', 'w'); open(f.fileno()) # OK
open(open('/tmp/b', 'w').fileno())        # KO - cf. http://hondu.co/blog/open-and-python

echo $SHELL                                            # /bin/bash
python -c "import os; print(os.environ.get('SHELL'))"  # None

class CustomHash:
    def __init__(self, hash): self.hash = hash
    def __hash__(self): return self.hash
CustomHash(1) in [CustomHash(1)]  # False, because "in" uses id(obj)

urllib.request.urlopen(url).read()
env['HTTPS_PROXY'] = ...
urllib.request.urlopen(url).read()  # Ignores proxy, require a call to urllib.request.install_opener(None) beforehand

a = a[0] = {}  # creates a self-referential dict - https://susam.in/blog/peculiar-self-references.html

hash(-1) == hash(-2)


"""""""""""""""""""""""""
"" Functional Programming
"""""""""""""""""""""""""
# Guido van Rossum is not a big fan, he wrote the very interesting 'The fate of reduce() in Python 3000'

# Buitins
apply, map, filter, zip # I agree with GvR that a list-comprehension is often clearer than a call to filter
from functools import partial, reduce # for Py3+ compatibility
sum(list_of_lists, []) # flatten a list of lists - Alt: list(itertools.chain.from_iterable(l_o_l)) OR reduce(operator.concat, l_o_l)

# Extra libs
dakerfp/patterns # functional pattern matching through real DSL made by modifying the AST ; http://www.slideshare.net/dakerfp/functional-pattern-matching - Alt: santinic/pampy - Also with Py3.10+: https://www.hillelwayne.com/post/python-abc/
toolz # brings: pluck, tail, compose, pipe, memoize - Even faster: CyToolz
suor/funcy
kachayev/fn.py

JulienPalard/Pipe # fib() | where(lambda x: x % 2 == 0) | take_while(lambda x: x < 4000000) | add

visitor # tiny library to facilitate visitor pattern implementation


"""""""""""""""""""""""""
"" Subprocesses & shell
"""""""""""""""""""""""""
xonsh # Python3-ish, BASHwards-looking shell language - Alt: ergonomica
# grep-like one-liners:
python -c 'import sys, re; sys.stdout.writelines([str(re.search("REGEX", line).groups())+"\n" for line in sys.stdin])'

from distutils import spawn
cmd_path = spawn.find_executable('cmd') # shutil.which in Python3 / shutilwhich backport else
subprocess.check_output([cmd_path, 'do', 'stuff'], input=bytes(some_text, 'UTF-8')) # last param added in 3.4 : https://hg.python.org/cpython/file/877f47ca3b79/Lib/subprocess.py#l614
# AVOID PIPE ! Flaws & workarounds: http://www.macaronikazoo.com/?p=607 ; http://eyalarubas.com/python-subproc-nonblock.html
# -> I was bitten by PIPE in Cygwin: cf. pre-commit issue 379
kennethreitz/delegator.py # handy subprocesses lib

platform # python version, OS / machine / proc info...
appdirs # determine appropriate platform-specific user data/config/cache/logs directory paths
resource # limit a process resources: SPU time, heap size, stack size... Example of context manager to limit memory usage: http://stackoverflow.com/a/14024198
.setrlimit(RLIMIT_AS, (size, hard)) / .setrlimit(RLIMIT_CPU, (seconds, hard)); signal(SIGXCPU, time_exceeded)  # cf. https://martinheinz.dev/blog/1

shlex.split('--f "a b"') # tokenize parameters properly
pipes.quote() # to escape variables - Alt: shlex.quote() for Python3.3+

lordmauve/chopsticks # orchestration library to configure & control remote hosts over SSH
supervisor # process control system for UNIX

### sh.py tips & tricks
# Caveat: does not work under Windows
# Alt (but less pythonic/simple IMHO): gawel/chut, plumbum, sarge
# Special keyword args: https://amoffat.github.io/sh/special_arguments.html#special-arguments
- all commands are checked at 'from sh import' time so they are guaranteed to exist
- Always use `_err=sys.stderr` or `_err_to_out=True` because default is to discard commands stderr
- `print()` is NEEDED to display command output (or you need to use `_out=sys.stdout`)
- `_piped='direct'` is useful to connect processes without consuming any memory
- `_iter` : creates a line generator => you can chain lazy functions taking a 'input_iterator' as input & output
- a command invocation return a `RunningCommand` object, on which you can wait for the text output (by calling `str()` on it)
or get a list of output lines (by calling `list()` on it)

import sh, sys
if sys.version_info[0] < 3:
    sh = sh(_err=sys.stderr, _out=sys.stdout)  # setting default commands redirections
else:
    sh = sh(_err=sys.stderr.buffer, _out=sys.stdout.buffer)  # Accessing the .buffer is needed under Python 3, cf. https://github.com/amoffat/sh/issues/242
sh.bzcat(...)
with open(filename, 'a') as file:
    sh.ls(_out=file) # to append stuff at the end, aka >>

if len(argv) > 1:
    pipe = cat(argv[1], _iter=True, _err=stderr)  # `pipe` is an input_lines_iterator
else:
    pipe = cat(_in=stdin, _iter=True, _err=stderr)

(import [sh [cat grep wc]]) # in Hy, aka Python with Lisp syntax
(-> (cat "/usr/share/dict/words") (grep "-E" "^hy") (wc "-l"))


"""""""""""""""""""""""""
"" Libs & tools for DEVS !
"""""""""""""""""""""""""
PYTHONWARNINGS=error # sets this when developing !
# Cheap virtualenv - Alt: mitsuhiko/pipsi -> each pkg is installed into its own virtualenv, so you don't have to worry about different packages having conflicting dependencies
PYTHONUSERBASE=.pip/ pip install --user $pkh
PYTHONUSERBASE=.pip/ python -m $pkg
pew > virtualenv # sandbox. To move an existing environment: virtualenv --relocatable $env
guyzmo/buildstrap # to create a standalone buildout environment (~ virtual env)

~/.jenkins/shiningpanda/jobs/$i/virtualenvs/$id/bin/activate # Path of virtualenvs generated by Jenkins plugin ShiningPanda
api4jenkins  # Alt, already used but less maintained: jenkinsapi
buildbot # CI framework - Pipeline example: https://github.com/buildbot/buildbot/blob/master/master/buildbot/scripts/sample.cfg - Alt: Jenkins (Groovy)

pip install --editable $path_or_git_url # Install a project in editable mode (i.e. setuptools "develop mode") from a local project path or a VCS url. FROM: S&M
pip install --user $USER --src . --no-index --no-deps --no-cache-dir --upgrade --upgrade-strategy eager --requirement requirements.txt --require-hashes # CLI tool to help with retrieving correct hashes : hashin
pip freeze > requirements.txt # dumps all the virtualenv dependencies - Alt: pipdeptree to show the dependency tree of packages - Also, programatical access: pip.operations.freeze.freeze
pip-review # check for updates of all dependency packages currently installed in your environment : Alt: pip list --outdated --not-required ; piprot requirements.txt ; ./manage.py pipchecker
pip top-level requirements override sub-dependency ones  # full resolver logic : https://github.com/pypa/pip/issues/988
pyproject.toml # PEP-518 replacement for setup.py - Alt: https://github.com/pypa/pipfile by kennethreitz
pip install build && python -m build
python setup.py check --strict  # validate meta-data, ensuring all required args are present - Also: python setup.py sdist bdist_wheel
pip-compile # recursively pin Python dependencies; part of pip-tools - Alt: pip freeze - pip2tgz "/var/www/packages" mypackage && pip install --index-url="file:///var/www/packages" mypackage
pipconflictchecker # pip-conflict-checker package, detect dependency versions conflicts
PyPRI # private Python index in the cloud to which you have total control of access.
http://www.watchman-pypi.com  # Effectively find upstream & downstream dependencies of a Pypi package - Alt: https://github.com/DavHau/pypi-deps-db / libraries.io

import pip
pip.main(['install', '--proxy=' + PROXY, 'requests==2.7.0', 'retrying==1.3.3', 'sh==1.11'])
assert list(search_packages_info(['pip-tools']))[0]['version'] == '1.6.5'

def pip_compile(reqfile_lines, pip_args=[], allow_all_external=True, allow_unverified=()):  # to use pip-compile (from pip-tools) programmatically
    from tempfile import NamedTemporaryFile
    with NamedTemporaryFile('w') as tmp_file:
        tmp_file.write('\n'.join(reqfile_lines))
        tmp_file.flush()
        from pip.req import parse_requirements
        from pip.download import PipSession
        constraints = list(parse_requirements(tmp_file.name, session=PipSession()))
    from piptools.scripts.compile import PipCommand
    pip_options = PipCommand()
    import pip
    pip.cmdoptions.make_option_group(pip.cmdoptions.index_group, pip_options.parser)
    import optparse
    pip_options.parser.add_option(optparse.Option('--pre', action='store_true', default=False))
    pip_options, _ = pip_options.parse_args(pip_args)
    from piptools.repositories import LocalRequirementsRepository, PyPIRepository
    repository = LocalRequirementsRepository(existing_pins=dict(), proxied_repository=PyPIRepository(pip_options))
    repository.finder.allow_all_external = allow_all_external
    repository.finder.allow_unverified = allow_unverified  # exhaustive list of pkg names listed in --find-links resources
    from piptools.resolver import Resolver
    resolver = Resolver(constraints, repository)
    results = resolver.resolve()
    return [str(ireq.req) for ireq in results]

pybuilder, invoke # build tools, like Makefile with many plugins
Yelp/undebt # tool for performing massive, automated code refactoring

coverage erase
coverage run --source=path/to/python/src -m any_module_eg_behave
coverage report # ASCII report - Alt: html, xml

csvoss/onelinerizer # Convert any Python 2 file into a single line of code
liftoff/pyminifier # code minifier, obfuscator, and compressor
therealOri/PolyLock # encryption (with chaeslib) + obfscation (fork of hyperion) + Code compilation (with nuitka)

pyflakes, pylint --generate-rcfile > .pylintrc # static analysis - Also: Flake8, openstack-dev/hacking, landscapeio/prospector, pylama (did not work last time I tried), google/yapf
seddonym/import-linter # define and enforce rules for the internal and external imports

pyreverse # UML diagrams, integrated in pylint
pinetr2e/napkin # write UML sequence diagrams

Dobiasd/enterprython # type-based dependency-injection
carta/flipper-client # feature flipping engine

joeyespo/grip # preview GitHub Markdown files locally before committing them
vaab/gitchangelog # creates a changelog from git log history - I configured it for keepachangelog.com format on the Hesperides project

Cookiecutter # creates projects from project templates, e.g. Django, OpenStack, Kivy... + in other languages !
lobocv/crashreporter # store and send crash reports directly to the developers


"""""""""""""
"" Security
"""""""""""""
# Security linters:
safety, snyk # report security vulnerabilities in dependencies
dxa4481/truffleHog, landscapeio/dodgy, Yelp/detect-secrets # detect credentials/passwords/secrets in source code - Also, in other languages : awslabs/git-secrets, auth0/repo-supervisor, zricethezav/gitleaks
Pysa # PYthon Static Analyzer from facebook/pyre-check - detect vulnerabilities in Python Web Applications: XSS, SQL injection, command injection, directory traversal...
openstack/bandit  # Python AST-based security linter
    echo -e "[bandit]\nexclude: my_proj/.eggs,my_proj/src/unittest"
    bandit --ini .banditrc --recursive my_proj/ # -lll to limit to HIGH severity issues
returntocorp/semgrep # static analysis tool for finding bugs, suggested in Gitlab pipelines by default
python-afl # find bugs by fuzzing input - cf. https://barro.github.io/2018/01/taking-a-look-at-python-afl/

flipkart-incubator/Astra # Automated Security Testing for Rest Api's
openstack/syntribos  # automated API security testing tool
sqlmap  # automatic SQL injection and database takeover tool
wapiti  # "fuzzer", performs "black-box" scans of a web application by crawling the webpages of the deployed webapp, looking for scripts and forms where it can inject data

PyRASP  # Runtime Application Self Protection package for Python-based Web Servers and cloud functions

pwntools # CTF framework and exploit development, designed for rapid prototyping

magic-wormhole  # get things from one computer to another, safely: text, files, directories


"""""""""""""
"" Packaging
"""""""""""""
cf. https://packaging.python.org

twine # pkg upload to Pypi - Con: requires cmarkgfm pkg which is a pain to install under Windows - Alt: hatch & poetry
zip -r ../myapp.egg # Make an .egg - You just need a ./__main__.py - See also: zipimport, pkgutil & zipapp to generates .pyz from v3.5 -> pyroma # gives a rating of how well a project complies with the best practices of the Python packaging ecosystem, primarily PyPI, pip, Distribute etc.
autopub # automatically publish package releases upon pull request merge

those "Python ZIP Applications" are associated to the Python executable under Windows
dh-virtualenv # the ultimate way of deploying python apps, over wheels & pex == self-contained executable virtual environments : carefully constructed zip files with a #!/usr/bin/env python and special __main__.py - see PEP 441
cx_freeze to make an EXE easily # cf. this example : https://www.reddit.com/r/Python/comments/4if7wj/what_do_you_think_is_more_difficult_in_python/
facebookincubator/xar # archiver packinging files into a single self-contained executable bundle, using SquashFS, apprently better than PAR archives
indygreg/python-build-standalone # produces self-contained, highly-portable Python distributions, containing also build artifacts (object files, libraries, etc)
BeeWare # Write your apps in Python and release them on iOS, Android, Windows, MacOS, Linux, Web, and tvOS using rich, native user interfaces

# Examples of Windows packaging
deluge-torrent # with bbfreeze + GUI with pygtk: http://git.deluge-torrent.org/deluge/tree/win32/deluge-bbfreeze.py#n31
tweecode/twine # with py2exe/py2app + GUI with wxPython
Kivy # package apps with PyInstaller
pyinstaller --onefile cli.py # Use --noupx under Windows - I successfully used this in a Gitlab CI, with upload to Artifactory
# A Travis CI build script example using wine (one may also require Xvfb): https://github.com/spesmilo/electrum/blob/master/contrib/build-wine/prepare-wine.sh
# Quoting https://github.com/pyinstaller/pyinstaller/wiki/FAQ#gnulinux on its limitations:
> The executable that PyInstaller builds is not fully static, in that it still depends on the system libc.
> [A] solution is to use a tool like StaticX to create a fully-static bundled version of your PyInstaller application.
pynsist # used by Sam & Max with nuitka (installer for non-web apps)
PyOxidizer # Build Portable Binaries of Python Applications: https://hynek.me/til/python-portable-binaries/

from distutils.command.build import build
class custom_build(build):
    def run(self):
        build.run(self)
        ... # custom init
cmdclass['build'] = custom_build

# VERSION: can a package version be only defined only in one place ?
__version__ in __init__.py + setup.py # PEP 396 compliant but both need to be kept in sync.
                                      # One can import __version__ in setup.py, but this should NOT mean
                                      # that the package must be installed for setup.py to be interpreted
__version__ = importlib.metadata.version(sys.modules[__name__]) # AttributeError: partially initialized module ... (most likely due to a circular import)
setuptools_scm, vcversioner  # manage your setup.py versions by scm tags


"""""""""""""
"" Testing
"""""""""""""
# `type()` can be an alternative for Nose tests, as TestCase and generators are not compatible
# Better is to simply create in a loop child classes of a parent TestCase that simply redefine the setUp method
# TestCase.subTest is an alternative if data is not common to all test methods in the TestCase
# Even more alternatives : http://stackoverflow.com/questions/2798956/python-unittest-generate-multiple-tests-programmatically

dir(__builtins__) # special module, and functions can be reassigned !
@patch("that_context_mgr", MagicMock(__enter__ = lambda *args: MyReturnedObject()))
@patch("module.open", create=True) # to patch builtins
@patch("module.CONSTANT", new_value)
def foo_test(open_mock):
    input_mock = MagicMock(spec=file)
    open_mock.return_value = input_mock
    input_mock.__enter__.return_value.readline.return_value = "ALWAYS SAME LINE"

obj_mock.side_effect = Exception('Foo42')

import faker # generate test data: phone numbers, IPs, URLs, md5 hashes, geo coordinates, user agents, code... - Alt: lk-geimfari/elizabeth
minimaxir/big-list-of-naughty-strings
import nose # -m nose.core -v -w dir --pdb --nologcapture --verbose --nocapture /path/to/test_file:TestCase.test_function - Also: http://exogen.github.io/nose-achievements/
nosetest # -vv --collect-only # for debug
py.test -vv --capture=no/-s --showlocals/-l --strict-config --strict-markers --exitfirst --cache-clear --pdb -m $marker -k 'TestClass and test_methode_name' # selective test execution - To set parameters by defaults, use the `addopts` entry in your config file
pytest -k "$(tq failure -p -a name < results.xml | awk 'NR>1{print(" or ")} {print}' ORS='')" # rerunning only failed tests, require --junit-xml=results.xml
    pytest-bdd, pytest-benchmark (can produces an histogram), pytest-cram, pytest-pythonpath, pytest-selenium, pytest-sugar # plugins - Also: memory leak detector https://nvbn.github.io/2017/02/02/pytest-leaking/
    pytest-timeout # abort hanging tests / ensure tests do not take too long to execute - Better alt: fpdf2 ensure_exec_time_below() decorator or time_execution() context-manager
    pytest-monitor # Analyze resources consumption (memory / time / CPU) & keep an history
    pytest-profiling # tests are profiled with cProfile and analysed with pstats; heat graphs are generated using gprof2dot and dot
    pytest-testmon # keeps track of which code is used by which tests, to only run the tests relevant for the changes made
    pytest-play # REST API testing based on YAMLs files
    pytest-icdiff # better, colored diffs in pytest assertion error messages using ICDiff
    pytest-watch # re-run tests when a file in your project changes
airspeed velocity # designed to benchmark a single project over its lifetime using a given set of benchmarks – i.e., little snippets of code that are timed - the result data is stored in JSON files
mschwager/memunit # check memory usage in tests - Better alt: fpdf2 ensure_rss_memory_below(): https://github.com/PyFPDF/fpdf2/blob/2.7.3/test/conftest.py#L263
self.assertRaisesRegexp / assertDictContainsSubset / assertAlmostEqual(expected, measured, places=7)
c-oreills/before_after # provides utilities to help test race conditions
import sure # use assertions like 'foo.when.called_with(42).should.throw(ValueError)'
import doctest # include tests as part of the documentation
AndreaCensi/contracts # Design By Contract lib - Alt: PythonDecoratorLibrary basic pre/postcondition decorator
behave # Behavior Driven Development (BDD) - Comparison with alts: https://pythonhosted.org/behave/comparison.html
import hypothesis # feed you test with known to break edge cases - "based on a fuzzer-kind of mechanics where data generation is based off a byte stream that can get higher or lower in complexity"

import capsys # capture stdin/out
with capture_stderrout() as (stdout, stderr): # Recipe from http://stackoverflow.com/a/17981937/636849

brodie/cram # generic command-line (CLI) app testing - Alt: Bats (TAP-compliant, bash), autoexpect, Tush, Aruba
Pexpect # interact with programs based on expected stdout outputs - Include pxssh to interact with ssh: login()/logout()/prompt()
ptyprocess # launch a subprocess in a pseudo terminal (pty) and allow read/write to it


"""""""""""""
"" Debugging
"""""""""""""
faulthandler.enable() # dump stacktrace on SIGSEGV, SIGABRT... signals ; python2 -X faulthandler script.py

python -mtrace --ignore-module=codeop,__future__ --trace [ $file | $code_module_path ] # trace all code lines run when executing a file / in interactive console
dhellmann/smiley # application tracer, record & report, inspired by rad2py/wiki/QdbRemotePythonDebugger

python -mtimeit -s'xs=range(10)' '[hex(x) for x in xs]' # exec time, compare to 'map(hex, xs)'
timeit.timeit(local_func, setup="from m import dostuff; dostuff()", number=1000)

python -m cProfile -o output.pstats script.py # cProfile.Profile().dump_stats('output.pstats')
from pstats import Stats; stats = Stats(); stats.add('output.pstats'); stats.sort_stats('cumulative'); stats.print_stats()
gprof2dot.py -f pstats output.pstats | dot -Tpng -o output.png
pycallgraph graphviz -- ./mypythonscript.py # Alt for recursion tree: carlsborg/rcviz
kernprof --line-by-line myscript.py # from line_profiler pip package, great but does not support Cygwin
pyprof2calltree # use kcachegrind
python-flamegraph # FlameGraph profiler
P403n1x87/austin # frame stack sampler for CPython
https://tech.dropbox.com/2012/07/plop-low-overhead-profiling-for-python/ # like gperftools, sampling profiler for prod servers
py-spy # sampling profiler, lets you visualize what your Python program is spending time on without restarting the program, with low overhead
http://mg.pov.lt/objgraph # explore Python object graphs: objgraph.show_most_common_types(limit=30)
yappi # multithread/CPU time profiling
snakefood # draw code base dependency graphs
what-studio/profiling # interactive continuous/live CLI profiler
PyVmMonitor # profiler with graphs
nschloe/tuna # profile viewer using tornado
nvdv/vprof # Visual Python profiler
emeryberger/scalene # a high-performance, high-precision CPU, GPU and memory profiler - Ex: https://www.reddit.com/r/Python/comments/s1oqb7/that_time_i_optimized_a_python_program_by_5000x/
StackImpact Python Agent # production profiler: CPU, memory allocations, exceptions, metrics
objgraph.show_most_common_types() # summary of the number objects (by type) currently in memory
        .get_leaking_objects() # objects in memory that do not have any other objects pointing at them
        .show_backrefs(obj, max_depth=10) # Usage example: https://benbernardblog.com/tracking-down-a-freaky-python-memory-leak/
libleak > memleax # utility producing a report of C call stacks where a process memory allocations are not matched by deallocations - Demo + LD_PRELOAD usage: https://web.archive.org/web/20210227012641/https://info.cloudquant.com/2018/12/numpyleaks/
cProfile + psutil.Process().num_ctx_switches # cf. https://pythonspeed.com/articles/custom-python-profiler/
sys._debugmallocstats()  # print summary info to stderr about the state of Pymalloc's structures - paulross/pymemtrace allows to extract the information it contains
import tracemalloc # Python3, stats on allocated memory blocks per filename & line number - Requires -X tracemalloc - Recipes: https://confluence.desy.de/display/FSEC/Finding+memory+leaks & https://stackoverflow.com/a/45679009/636849
fabianp/memory_profiler # track the memory usage of a program line by line in the source code - require psutil => not usable with Cygwin - Tuto: https://medium.com/zendesk-engineering/hunting-for-memory-leaks-in-python-applications-6824d0518774
    from pympler.muppy import get_objects, getsizeof
    from pympler.summary import print_, summarize
    from pympler.util.stringutils import pp
    from psutil import Process
    print("[psutil] process memory:", pp(Process().memory_info()[0]))
    all_objects = get_objects()
    objs_size_sum = sum(getsizeof(obj) for obj in all_objects)
    print("[pympler/muppy] sum of objects memory size:", pp(objs_size_sum)) # usually a lot lower than the actual process memory usage :(
    print_(summarize(all_objects))
from guppy import hpy
h = hpy()
h.heap()
h.iso(...objects...).sp
# Also: http://stackoverflow.com/questions/938733/total-memory-used-by-python-process
asizeof # the simplest solution from: https://pympler.readthedocs.org/en/latest/related.html
print('Memory usage:', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000, 'MB')  # peak process memory usage - unit: https://stackoverflow.com/questions/938733/total-memory-used-by-python-process#comment35291064_7669482 - but BEWARE: this value does not make sense in a containerized env (I witnessed it with a Python process in Docker: the host did not allocated those >1Go)
rogerhu/gdb-heap  #  Heap Analyzer for Python
bcc/PyPerf # eBPF-based Python profiler https://github.com/iovisor/bcc/blob/master/examples/cpp/pyperf/PyPerf.cc - Related talk & vid: https://granulate.io/blog/python-application-profiling-ebpf/

import gc; gc.get_objects() # Returns a list of all objects tracked by the garbage collector -> SUPER powerful to hack python code and sniff values

from rfoo.utils import rconsole # RPC remote debugging - Alt: signal-based handle on a program to debug: http://stackoverflow.com/a/133384/636849
rconsole.spawn_server()
$ rconsole
# And also: http://eventlet.net/doc/modules/backdoor.html

# IPython tricks - Alt REPL: ptpython
cd /a/path
!cmd # shell command
%quickref
%load script.py # and %%file to write to a file
%save $filename # save session - Alt: %history -> dump it. Stored in ~/.config/ipython/profile_default/history.sqlite - used by pdb too
%paste # if it fails because Tkinter is not available, use %cpaste
%pdb # Automatic pdb calling
%timeit do_something()
%debug # post_mortem
%bg # run in the background
%load_ext autoreload & %autoreload 2 # reload all changed modules every time before executing a new line. Some caveats apply, type %autoreload? to see what can go wrong
%%javascript # and many other languages
from IPython.display import HTML, SVG; HTML(html_string) # render HTML, SVG
ipython notebook # now Jupyter - D3 support : wrobstory/sticky - Interesting "static" alts: janschulz/knitpy & pystitch/stitch
ipython nbconvert --to [html|latex|slides|markdown|rst|python]
jq -r '.worksheets[0].cells[].input' < $file.ipynb # Alt JSON query language: jmespath

from io import BytesIO
img_bytes = BytesIO(); img.save(img_bytes, format='png')  # img is a PIL.Image
from base64 import b64encode
img_base64 = b64encode(img_bytes.getvalue()).decode('utf-8')
from IPython.display import HTML
HTML('<img src="data:image/png;base64,{0}"/>'.format(img_base64))

# PDB tricks
~/.pdbrc # to persist history: https://stackoverflow.com/a/35866289/636849
import sys; from subprocess import call; call(['/usr/bin/bash'], stderr=sys.stderr, stdin=sys.stdin, shell=True) # launch an interactive Bash session
!p = ... / !list(...) # make it possible to start a cmdline with pdb commands
!import code; code.interact(local=vars()) # simply `interact` in Python 3
debug foo() # step into a function with pdb
import sys, pdb, traceback; error_msg = ''.join(traceback.format_exception(*sys.exc_info())); pdb.set_trace() # to use in an `except` block to capture the stacktrace
from IPython.core.debugger import Pdb; Pdb().set_trace()
ipdb.set_trace() / python -mipdb / ipdb.pm() / ipdb.runcall(function, arg)
zestyping/q  # quick and dirty debugging that inc. time : q/ & q| @q (inc. return values) q.d() (~pdb)
pdbpp # prettier PDB
google/pyringe # when python itself crashes, gets stuck in some C extension, or you want to inspect data without stopping a program
import rpdb; rpdb.set_trace() # remote debugging - Alt: python-web-pdb
from pdb_clone import pdb; pdb.set_trace_remote() # then pdb-attach : remote-debugging - Also: pdbhandler.register() to enter at any time a running program
pyrasite # attach to a running Python process, e.g. https://gist.github.com/simonw/8aa492e59265c1a021f5c5618f9e6b12
boltons.debugutils.pdb_on_signal

from pprint import pprint # indent=4
vars(obj), dir(obj)

[modname for importer, modname, ispkg in pkgutil.iter_modules(mypkg.__path__)] # list modules of package
inspect.getmembers(obj)
inspect.getargspec(foo_func) # get signature
inspect.getfile(my_module)
inspect.getsource(foo_func) # if implemented in C, use punchagan/cinspect
frame,filename,line_number,function_name,lines,index=inspect.getouterframes(inspect.currentframe())[1]
inspect.currentframe().f_back.f_globals['foo'] = 'overriding caller local variable!'  # ONLY works with f_globals, not f_locals (unless they are equal) due to the FASTLOCALS cache / instruction

def get_instance_var_name(method_frame, instance):
    parent_frame = method_frame.f_back
    matches = {k: v for k,v in parent_frame.f_globals.items() if v is instance}
    assert len(matches) < 2
    return matches.keys()[0] if matches else None
class Bar:
    def foo(self):
        print get_instance_var_name(inspect.currentframe(), self)
bar = Bar(); bar.foo(); nested = lambda: bar.foo(); nested(); Bar().foo()
# Alt, even more robust: use parent_frame.f_code.co_code & the dis module

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

code = "my code bla bla"
compiled = compile(code)
exec compiled

from dis import dis; dis(myfunc) # get dissassembly - Also, to extend Python with x86 asm modules: https://p403n1x87.github.io/python/assembly/2018/03/23/asm_python.html
uncompyle2 prog.pyc # bytecode -> python code
from elftools.elf.elffile import ELFFile # eliben/pyelftools - parse ELF and DWARF formats
capstone # multi-platform, multi-architecture disassembly framework

neuroo/equip # bytecode instrumentation, e.g. insert call counters logic into .pyc
foo.func_code = marshal.loads(marshal.dumps(foo.func_code).replace('bar', 'baz')) # bytecode evil alteration
astor / astunparse # AST 'unparse' : tree -> source
ast.literal_eval # safe eval of a basic string expression: "it is not capable of evaluating arbitrarily complex expressions, e.g. involving operators or indexing"
pyrser # easy Python AST transformations, with CSS-like selectors

def get_refcount(obj):
    """Valid for CPython implementation only"""
    return ctypes.c_size_t.from_address(id(obj))
# FUN FACT: the references to the 'int' [-5 ; 256] are shared
ctypes.POINTER(c_int).from_address(0)[0] # SEGFAULT
def deref(addr, typ):
    return ctypes.cast(addr, ctypes.POINTER(typ))
deref(id(42), ctypes.c_int)[4] = 100 # change value of 42 ! - '4' is the index to the ob_ival field in a PyIntObject - In Python3 this index is '6'
x = lambda: None; y = type(x.__code__)(0, 0, 0, 0, 0, b'\x01', (), (), (), '', '', 0, b''); type(x)(y, {})() # SEGFAULT


"""""""""""""""""""""""""""""""
"" Libs & tools for SCIENCE !
"""""""""""""""""""""""""""""""
nltk, TextBlob # Text analysis : noun phrase extraction, sentiment analysis, translation...
LuminosoInsight/wordfreq # Access a database of word frequencies, in various natural languages.
topia.termextract # keywords extraction (2 lines broken under Py3, cf. my fork) - Alt: rake (2 implementations exist)
difflib # compare text/strings/sequences
fuzzywuzzy # fuzzy string comparison ratios, token ratios, levenstein distance... Alt: maxbachmann/RapidFuzz
sumy # text summarization - Install: sudo aptitude install libxml2-dev libxslt1-dev && pip install sumy && python -m nltk.downloader -d /usr/share/nltk_data all # 1.7GB
goose3 # take any news article or article-type web page and not only extract what is the main body of the article but also all meta data and most probable image candidate
deanmalmgren/textract # extract text from .doc .gif .jpg .oft .pdf .png .pptx .ps ... Alt for PDF: euske/pdfminer/blob/master/tools/pdf2txt.py
from pdfminer.high_level import extract_text, LAParams  # from pdfminer.six
extract_text(pdf_filepath, page_numbers=[0], laparams=LAParams(char_margin=5))  # this param is useful for lines of text is words far apart
snowballstemmer # supports 15 languages
ahocorasick, acora # Aho-Corasick automaton : quick multiple-keyword search across text
vi3k6i5/flashtext # Extract Keywords from sentence or Replace keywords in sentences
superelasticsearch # provide iterated search & simpler bulk API
lunr # parses a set of documents and creates an inverted index for quick full text searches

decimal.Decimal # contrary to floats : 3*0.1 - 0.3 == 0.0
fractions
statistics # Python 3 or pypi/statistics backport - Alt: simplestatistics
kwgoodman/roly # moving window median algorithms - Alt: ajcr/rolling: computationally efficient rolling window iterators - Also: quantile sketches algos in Algo_Notes.md

numpy # n-dimensional arrays, vectorized operations and broadcasting : faster than CPython for large arrays
    Illustrated Guide: https://betterprogramming.pub/numpy-illustrated-the-visual-guide-to-numpy-3b1d4976de1d
    SciPy  # collection of mathematical algorithms and convenience functions built on NumPy
sympy # symbolic mathematics: formula printing (also: PyLatex), simplification, equations, matrices, solvers...
SageMath # open-source mathematics software system built on top of NumPy, SciPy, matplotlib, Sympy, Maxima, GAP, FLINT, R and many more
pandas, sql4pandas # data analysis, to go further : statsmodels, scikit-learn or PyMC (Machine Learning), orange (dedicated soft for visu), miha-stopar/nnets (neural networks)
    pd.read_html(url, header=0, parse_dates=["Call Date"]) # extract table from HTML page into a DataFrame
    JosPolfliet/pandas-profiling # -> create HTML profiling reports from pandas DataFrame objects, inc. quantiles, most frequent values, histograms & descriptive statistics
    agate # data analysis library optimized for humans, not machines; alternative to numpy and pandas that solves real-world problems with readable code
ortools # Google Operational Research tools:
  # * Constraint Programming - CP-SAT solver: A constraint programming solver that uses SAT (satisfiability) methods. - Original CP solver: A constraint programming solver.
  # * Linear and Mixed-Integer Programming - Glop: A linear optimizer to find the optimal value of a linear objective function, given a set of linear inequalities as constraints. - MPSolver, ModelBuilder: Wrappers around commercial and other open source solvers, including mixed integer solvers: CBC, CLP, GLPK, Gurobi or SCIP.
  # * Graph Algorithms Code for finding shortest paths in graphs, min-cost flows, max flows, and linear sum assignments.
OpenAI Gym # toolkit for developing and comparing reinforcement learning algorithms
matplotlib, prettyplotlib, mpld3, bokeh, plotly, glue, vispy, vincent (d3.js), seaborn, pygal, folium (-> Leaflet.js maps, cf. http://python-visualization.github.io/folium/)
    Pylab = matplotlib.pyplot + NumPy
    prettymaps  # draw customized maps from OpenStreetMap data
    Pyqtgraph  # "when you really want to plot a million points on the screen without the computer crying"
pyecharts # line charts, bars, pie, map, radar, graphs, trees, treemaps, sunburst, gauge, calendars, 3D
geoplotlib, ResidentMario/geoplot
ResidentMario/missingno, holoviews, pascal-schetelat/Slope # other dataviz libs
yhat/ggplot # data visualisation 2d graphing/plotting - Also: pyplot.xkcd() is awesome - Also: has2k1/plotnine
(ggplot(mtcars, aes('wt', 'mpg', color='factor(gear)'))
 + geom_point()
 + stat_smooth(method='lm')
 + facet_wrap('~gear')
 + theme_xkcd())

hickford/primesieve-python # one of the fastest prime sieve implementaions (C++)

z3-solver # SMT (satisfiability modulo theories) solver
    https://ericpony.github.io/z3py-tutorial/guide-examples.htm
    How I Cheat at Maths - Z3 101 by chown in Phrack #69
kiwisolver # a set of contraints that can be either equalities or inequalities (>= and <=), each of which can have an associated strength making more or less important to respect when solving the problem

AtsushiSakai/PythonRobotics # filter localization / grid mapping / object shape recognition / SLAM - closest point matching / path planning / path tracking
jhcepas/ete # tree exploration & visualisation
riccardoscalco/Pykov # markov chains

SimpleCV # powerful computer vision tools : find image edge, keypoints, morphology; can use the Kinect
sikuli # Java-based (with JS, Python & Ruby ports) visual workflow, able to identify images on screen using OpenCV
python-graph-core, networkx, igraph, graph-tool # networks & graphs manipulation

deap # genetic programming
cvxopt # convex optimization
eyounx/ZOOpt # Zeroth-Order optimization (a.k.a. derivative-free optimization/black-box optimization) does not rely on the gradient of the objective function, but instead, learns from samples of the search space. It is suitable for optimizing functions that are nondifferentiable, with many local minima, or even unknown but only testable.

joblib # memoize computations by keeping cache files on disk
petl # extract, transform and load tables of data (ETL)
@ratelim..patient # themiurgo/ratelim: limits the number of times a function is called during a time interval

rpy2 # acces to R + cf. https://www.dataquest.io/blog/python-vs-r/


"""""""""""""""""""
"" High perfs & C
"""""""""""""""""""
Shaarli: https://chezsoi.org/shaarli/?searchtags=performances+Python

Optimization guide:
- measure first (line_profiler !)
- improve algorithms ? data structures (for lightweight objects, use namedtuples) ? use a cache ?
- Numba (faster than Cython, which is faster than Pypy) + Numpy (vectorized operations are way faster than Pyhton slow loops - use: ufuncs, aggregates, broadcasting, slicing & masking)
- try Pypy or taichi

Using a C++ library in a Python script # one-page tutorial in Page Out #4
Cython # .pyx : superset of Python with optional static types, can invoke C/C++ and compile down to C
    AlanCristhian/statically : provides the @statically.typed decorator to compile a Python function with Cython
    fast_crash.pyx # nice Cython multiprocessing (OpenMP) code sample from "Personalized PGP Key IDs for fun and profit" by Filippo Valsorda in Phrack #69
PyPy # can be faster, compiles RPython code down to C, automatically adding in aspects such as garbage collection and a JIT compiler, but does not support C extensions. Also: PyPy-STM
exaloop/codon # high-performance Python compiler that compiles to native machine code. Typical speedups are on the order of 10-100x
from jitpy.wrapper import jittify # fijal/jitpy : embed PyPy into CPython, can be up to 20x faster
Jython / Py4J # intercommunicate with Java -> Jython has pip, but won't support lib depending on multiprocessing - however, it has excellent support for built-in Java threads: http://www.jython.org/jythonbook/en/1.0/Concurrency.html
voc # transpiler converting Python code into Java bytecode
Numba # NumPy aware dynamic Python compiler using LLVM - Also: numbapro # for targeting the GPU & writing CUDA code in Python
taichi # Python subest for parallel programming / high-performance numerical computation with just-in-time (JIT) compiler to offload compute-intensive code to the GPU or CPU - https://docs.taichi-lang.org/blog/accelerate-python-code-100x
    supports multiple data types, including struct / dataclass / quant / sparse, and allows you to adjust memory layout flexibly
Pyston # VM using LLVM JIT
Pythran # Python to c++ compiler for a subset of the Python language. It takes a Python module annotated with a few interface description and turns it into a native python module with the same interface, but (hopefully) faster.
PyInline # put source code from other programming languages (e.g. C) directly "inline" in Python code
Pyrex # write code that mixes Python and C data types and compiles it into a C extension
Nuitka # converts Python code into C++ code (targetting VisualStudio, MinGW or Clang/LLVM compilers)

pgiri/pycos # asynchronous, concurrent, network, distributed programming and distributed computing, using tasks, generator functions, asynchronous completions and message passing
pgiri/dispy # distributed and parallel computing framework, in a cluster, grid or cloud -> well suited for data parallel (SIMD) paradigm

classner/pymp # easy, OpenMP style multiprocessing on Unix (only work on systems with fork support)

ctypes.cdll.LoadLibrary("libc.so.6")
libc = ctypes.CDLL("libc.so.6")
libc.printf("An int %d, a double %f\n", 1234, ctypes.c_double(3.14))
pefile # to read Portable Executable files, e.g. Windows .dll

# Calling C or C++ From Python: https://realpython.com/python-bindings-overview/
cffi # C Foreign Function Interface for Python : call compiled C code from interface declarations written in C
pybind11 # Seamless operability between C++11 and Python - Also: cppimport : Import C++ files directly from Python

https://tech.blue-yonder.com/oxidizing-python-speeding-up-urlquoting-by-using-rust/ # writing a C-Library in Rust and invoke it from Python with cdylib, cbindgen, milksnake & cffi
pyduktape # evaluate JS from Python, used in Undying Dusk

struct # pack/unpack binary formats
binascii.hexlify # display binary has hexadecimal

mmap # memory-mapped files

# C-API -> good tuto for calling Python from C: https://learning-python.com/class/Workbook/unit16.htm


"""""""""""""""""""""""""""""""
"" DBs, queues & schedulers
"""""""""""""""""""""""""""""""
celery # distributed task queue - Monitoring: mher/flower - Alt: pyres, huey & rq (both based on Redis) - Also: celery_once to prevent multiple execution and queuing of tasks + https://www.distributedpython.com/2018/07/03/simple-celery-setup/
ampqlib, haigha, puka, aio_pika # AMPQ libs
kombu (based on celery), zeromq, aiozmq, mrq # distributed app / msg passing frameworks
dask  # task scheduling and blocked algorithms for parallel processing
sched # event scheduler - Alt: fengsp/plan, crontabber, thieman/dagobah, dbader/schedule, python-crontab, gjcarneiro/yacron, gawel/aiocron, jhuckaby/Cronicle (NodeJS with web UI)

luigi # workflow managers - Alt: Oozie, Azkaban, Drake, Pinball, viewflow, BD2KGenomics/toil, Apache Airflow -> prez: http://events.linuxfoundation.org/sites/events/files/slides/get_in_control_of_your_workflow.pdf
# the `luigid` daemon should be stopped with the `kill` command that sends a `SIGINT` signal so that it can save its state into `luigi-state.pickle` (cf. https://github.com/spotify/luigi/blob/master/luigi/server.py#L277)
csurfer/pypette # very simple flow controller for building complex pipelines

kibitzr # poll web pages and notify you in messenger or by e-mail

mrjob # run MapReduce jobs on Hadoop or AWS
robinhood/faust # stream processing library, porting the ideas from Kafka Streams to Python

kennethreitz/records # by the author of requests
peewee, SQLAlchemy # ORM DB - USeful: absent1706/sqlalchemy-mixins
from playhouse.sqlite_ext import SqliteExtDatabase; db = SqliteExtDatabase(':memory:') # in-memory SQLite DB with peewee
anydbm: dbhash else gdbm else dbm else dumbdbm
sqlite3 # std DB, persistent in a file || can be created in RAM - Alt: rogerbinns/apsw +> both allow to create custom SQL functions, aggregate functions, and collations
asyncpg # PostgreSQL without the need for libpq, faster than psycopg2
python-lsm-db(like LevelDB), unqlite-python(like MongoDB), vedis-python(like Redis) # Other embedded NoSQL DBs
pyMySQL, noplay/python-mysql-replication
stephenmcd/hot-redis, getsentry/rb, closeio/redis-hashring, fengsp/rc.Cache, coleifer/walrus
pylibmc # memcache client in C
redash # generic DB interface / visualization for Redshift, Google BigQuery, PostgreSQL, MySQL, Graphite, Presto, Google Spreadsheets, Cloudera Impala, Hive
cmu-db/ottertune # automatic DBMS configuration tool
jeffknupp/sandman2 # automatically generate a RESTful API service for your legacy database


"""""""""""""""""""""""""""""""
"" CLI & arguments parsing
"""""""""""""""""""""""""""""""
twobraids/configman > argparse (with fromfile_prefix_chars='@' to allow arguments definition in a @file) > optparse # Alt: begins > docopt, clize, click - Also: neat quick GUI compatible with argparse: chriskiehl/Gooey
class ArgparseHelpFormatter(argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter): pass
class ArgparseHelpFormatter(argparse.RawTextHelpFormatter):
    def _get_help_string(self, action):  # Inspiré de ArgumentDefaultsHelpFormatter mais affiche les valeurs par défaut non-nulles
        if "%(default)" not in action.help and action.default not in (argparse.SUPPRESS, None):
            action.help += " (default: %(default)s)"
        return action.help
parser = argparse.ArgumentParser(description=__doc__, formatter_class=ArgparseHelpFormatter, fromfile_prefix_chars='@', parents=[parent_parser], conflict_handler='resolve', allow_abbrev=False)
parser_group = parser.add_mutually_exclusive_group(required=True)
parser_group.add_argument(... type=argparse.FileType('r')) # or with the helper func below: action=argparse_store_command(func_do_cmd1) and after parsing: args.command(args)
return parser.parse_args(sys.argv[1:])
def argparse_store_command(callback, attr_name='command'):
    class StoreCommandAction(argparse.Action):
        def __init__(self, option_strings, dest, nargs=0, **kwargs):
            super(StoreCommandAction, self).__init__(option_strings, dest, nargs=0, **kwargs)
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, attr_name, callback)
    return StoreCommandAction
def environ_or_required(key):  # FROM: https://stackoverflow.com/a/45392259/636849
    if os.environ.get(key):
        return {'default': os.environ.get(key)}
    return {'required': True}
parser.add_argument('--thing', **environ_or_required('THING'))

code.InteractiveConsole().interact() # interactive python prompt

argcomplete # command line tab completion, for bash & argparse
pyreadline, readline, rlcompleter, python-prompt-toolkit

termcolor, colorama # cross-platform colored terminal text
tqdm # KISS progress bar - Alt, maybe better: Minibar, rsalmei/alive-progress
tabulate (handles Markdown with tablefmt='pipe'), PrettyTable, Leviathan1995/Pylsy # pretty ASCII tables output
termgraph # terminal plotting of histograms / scatterplots from list of coordinates - Some (little less polished) alts: bashplotlib, tehmaze/diagram
urwid # console user interface lib - Alt: snack, NPyScreen
willmcgugan/rich # rich text and beautiful formatting in the terminal: pretty tables, progress bars, markdown, syntax highlighted source code, tracebacks


"""""""""""""
"" Graphics
"""""""""""""
pyglet # windowing and multimedia lib
pysoy # 3D game engine
ericoporto/fgmk # retro RPG Game Maker

Zulko/gizeh, Zulko/MoviePy, ManimCommunity/manim, jdf/processing.py (uses Jython) # Video & image (editing - MoviePy looks like the current best tool to make GIF / webm animations - MoviePy Examples: https://zulko.github.io/blog/2014/09/20/vector-animations-with-python/ - Also: https://github.com/1-Sisyphe/youCanCodeAGif
thoppe/pixelhouse # minimalist drawing library for making beautiful animations. Comes with beautiful gradients, instagram-like filters, and elastic transforms.
3b1b/manim # animation engine for explanatory math videos
pygst # GStreamer : media-processing framework : audio & video playback, recording, streaming and editing
itsKaspar/tomato # glitch AVI files
ryanfox/retread # detect reused frames in video
smacke/ffsubsync # automagically synchronize subtitles with video, based on libs srt & py-webrtcvad (WebRTC Voice Activity Detector), or auditok (Audio Activity Detection) as a fallback

imageio.mimsave('/movie.gif', images) # lib based on Numpy + Pillow, to read / write a wide range of image data, including animated images, video, volumetric data, and scientific formats
-> can be used with pygifsicle to build GIF images, cf. https://medium.com/swlh/python-animated-images-6a85b9b68f86
neozhaoliang/pywonderland/blob/master/src/wilson/maze.py # example of GIF generation

cairo # graphics library outputting .ps .pdf .svg & more
pikepdf # edit & validate existing PDFs, using qpdf - Tuto to extract info / rotate / merge / split / add watermark / encrypt: https://realpython.com/pdf-python/ & craft_pdf_with_remote_img.py
fpdf2 # generate PDFs from scratch - cf. https://github.com/MrBitBucket/reportlab-mirror/tree/master/docs & https://github.com/driscollis/reportlabbookcode
xhtml2pdf # generate PDF documents from HTML content, with automated flow control such as pagination and keeping text together - Alt: Kozea/WeasyPrint
camelot # extract tables from PDFs - require NumPy - webapp side project: excalibur
PyMuPDF # access links and bookmarks; render pages in raster & vector formats; search for text; extract fonts, text and images...
wand (ImageMagick binding), pillow > pil # Python Image Library
exif = {ExifTags.TAGS[k]: v for k, v in Image.open('img.jpg')._getexif().items()} # from PIL import Image, ExifTags - Alt for edit: piexif
pyexiv2 # images EXIF manipulation
python-thumbnails # generates images thumbnails, e.g. for your website
ufoym/cropman # face-aware image cropping
lincolnloop/python-qrcode > pyqrcode # use PIL > C++ & Java
requests.post('https://zxing.org/w/decode', files={'f': open('qr.png', 'rb')})  # able to decode more images than pyzbar / zbarlight in my experience
graphviz # graphs generation and export as images
colorsys # rgb / yiq / hls / hsv conversions
makkoncept/colorpalette # Flask/heroku app that extracts palette of dominating colors from image - Alt: LanceGin/haishoku

AAlib, legofy # ASCII/Lego rendering, cf. ascii_art_email.py
fogleman/Tiling # pavages - uses cairo
nuno-faria/tiler # create an image using all kinds of other smaller images
andersbll/neural_artistic_style # transfer the style of one image to the subject of another image
anishathalye/neural-style # an implementation of neural style in TensorFlow
ribab/quadart # producing quad-tree art
lucashadfield/speck # line art image renderer, like Joy Division's Unknown Pleasures album
ahmedkhalf/Circle-Evolution # Evolutionary Art Using Circles

Tkinter, EasyGui, guizero, EasyDialogs (MacOSX), optparse_gui (last update 2008)
Kivy # GUI inc. multi-touch support, packaged with PyInstaller
wxPython # port of C++ wxWidgets
ChrisKnott/Eel # simple Electron-like HTML/JS GUI apps - Alt: cztomczak/cefpython
curses # terminal dialogs/interface - Ex: https://gist.github.com/claymcleod/b670285f334acd56ad1c
PySide2 # access to the complete Qt 5.12+ framework
pywebview # lightweight cross-platform wrapper around a webview component to display HTML content in its own native GUI window - "packagable" with pyinstaller

pytesseract.image_to_string
JaidedAI/EasyOCR
jlsutherland/doc2text # OCR poorly scanned PDFs in bulk
fonttools # playing with font kerning: https://readevalprint.com/Schmelvetica.html

espeak-ng # open source speech synthesizer supporting 7+ languages, based on the eSpeak engine
Uberi/speech_recognition # speech recognition with support for CMU Sphinx / Google Speech Recognition / Google Cloud Speech API / Wit.ai / Microsoft Bing Voice Recognition / Houndify API / IBM Speech to Text
jiaaro/pydub # manipulate audio with a simple and easy high level interface (with ugly operator override)
demucs # hybrid source separation: separate drums, bass and vocals from the rest
antiboredom/audiogrep
playsound # pure Python, cross platform, single function module with no dependencies for playing sounds


"""""""""""""""""""""""""""""""""""""
"" Multi-threads/processes & async
"""""""""""""""""""""""""""""""""""""
# Raymond Hettinger Keynote on Concurrency: https://pybay.com/site_media/slides/raymond2017-keynote/intro.html
multiprocessing, Pyro > threading # as Python can only have one thread because of the GIL - Using multiprocessing => everything should be pickable
threading.Thread().deamon = True # The entire Python program exits when no alive non-daemon threads are left.
threading.Event # for threads communication, including stopping: Thread.run(self): while not self.stop_event: ...
# Kill a thread ? -> http://stackoverflow.com/a/325528/636849
from multiprocessing.dummy import Pool as ThreadPool # Threads following multiprocessing API
pool = ThreadPool(4); results = pool.map(foo, args); pool.close(); pool.join()
SimPy # process-based discrete-event simulation framework

select # efficient I/O
def _make_file_read_nonblocking(f):
    fd = f.fileno()
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
from gevent import monkey; monkey.patch_all() # Greenlets
saucelabs/monocle, libevent, libuv, Twisted # other ASync libs, that is :
# concurrency (code run independently of other code) without parallelism (simultaneous execution of code)
ReactiveX/RxPY # asynchronous and event-based programming using observable collections and LINQ-style query operators
python -m twisted.conch.stdio # Twisted REPL
@asyncio.couroutine # aka Tulip, std in Python 3.3, port for Python 2.7 : trollius
asyncio.ensure_future # GOTO -> considered harmful
dabeaz/curio # Python 3 alt implementation of coroutines, with a better design: https://veriny.tf/asyncio-a-dumpster-fire-of-bad-design/
aiofiles # local disk files read/write in asyncio applications

wakepy # cross-platform wakelock / keep-awake / stay-awake: keeping CPU awake OR keeping screen awake

# Things I Wish They Told Me About The Multiprocessing Module in Python 3, with code examples:
# * https://pyvideo.org/pycon-us-2019/things-i-wish-they-told-me-about-the-multiprocessing-module-in-python-3.html
# * https://www.cloudcity.io/blog/2019/02/27/things-i-wish-they-told-me-about-multiprocessing-in-python/
# #1: Don't Share, Pass Messages
# #2: Always clean up after yourself
# #3: Obey all Signals
# #4: Don't ever wait forever
# #5: Report, and log all the things

# Python 3.4+ DefaultSelector uses the best select-like function available on your system - cf. http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html


"""""""""""""""""""""""""""""""
"" Web: HTTP, HTML & networking
"""""""""""""""""""""""""""""""
autobanh, crossbar.io # WAMP in Python
pywebsocket, python-hyper/wsproto
import xmlrpc.client # XML-RPC via HTTP
server = xmlrpc.client.ServerProxy("http://www.pythonchallenge.com/pc/phonebook.php")
print(server.system.getCapabilities())  # Also: .listMethods() .methodSignature(...) .methodHelp(...)

miyuchina/mistletoe # Markdown parser with 100% CommonMark support - Alt: Python-Markdown/markdown (not CommonMark but used by pelican & has 3.4K GitHub stars), executablebooks/markdown-it-py (100% CommonMark), theacodes/cmarkgfm (beware issue #13), Hultner/safemd - focusing on security, e.g. to avoid XSS
templite, wheezy.template, mako, jinja2 # HTML template system - Note: {{"{{"}} escapes {{
mozilla/bleach # HTML sanitizing library that escapes or strips markup and attributes
tinycss2 > tinycss > cssutils  # CSS parsers
hickford/MechanicalSoup  # automate interaction with websites: handle cookies, redirects, links and forms, but not JavaScript
lxml > HTMLParser (std or html5lib), pyquery, BeautifulSoup # use v>=3.2 - also: defusedxml to sanitize XML
parser=lxml.html.HTMLParser(collect_ids=False)  # avoids a memory leak: https://benbernardblog.com/tracking-down-a-freaky-python-memory-leak-part-2/
kovidgoyal/html5-parser # fast C based HTML 5 parsing

import lxml.etree, lxml.html
html_root = lxml.html.fromstring('html string') # Alt: html_tree.getroot()
html_tree = lxml.etree.ElementTree(html_root) # Alt: lxml.etree.parse(some_file_like_object)
html_tree.getpath(element)
element.getparent().remove(element)
BeautifulSoup('html string').prettify() # newlines+tabs formatted dump - Alt, less pretty: lxml.html.tostring(element, pretty_print=True) / lxml.etree.tostring
for elem in xml_tree.xpath('//*[count(ancestor::*)>2]'): # truncating the tree
    elem.getparent().remove(elem)
with open('my_schema.xsd', 'rb') as xsd:
    xsd_schema = etree.XMLSchema(etree.parse(xsd))
parser = etree.XMLParser(schema = xsd_schema, dtd_validation=True, remove_blank_text=True) # the last parameter is needed for pretty_print to work - Also, by default: no_network=True
with open('my_data.xml', 'rb') as xml:
    etree.parse(xml, parser) # validate that data is conform to XSD schema + DTD structure

KNOWN_HTML_ATTRS = defs.link_attrs | defs.event_attrs | defs.safe_attrs | frozenset(['content', 'http-equiv', 'placeholder', 'role'])
def iter_html_non_standard_attributes(html_file):
    for _, elem in lxml.etree.iterparse(html_file, html=True, remove_comments=True):
        attribute_names = elem.attrib.keys()
        for attribute_name in attribute_names:
            if not any([attribute_name in KNOWN_HTML_ATTRS,
                        attribute_name.startswith('data-'),
                        attribute_name.startswith('aria-')]):
                yield attribute_name

urlparse.urljoin, urllib.quote_plus # urlencoding & space -> +
try:
    with urllib.request.urlopen(url) as response:
        return json.load(response)['version_id']
except urllib.error.HTTPError as http_error:
    if http_error.code == 404:
        return None
    raise
def http_do(verb, url, basic_auth_creds=None, timeout_in_secs=5, json_payload=None, parse_json=False):  # useful in AWS lambdas
    data = json.dumps(json_payload).encode('utf8') if json_payload else None
    req = urllib.request.Request(url, method=verb, data=data)
    if basic_auth_creds:
        encoded_creds = base64.b64encode(('%s:%s' % basic_auth_creds).encode('utf-8'))
        req.add_header('Authorization', 'Basic %s' % encoded_creds.decode('utf-8'))
    try:
        with urllib.request.urlopen(req, timeout=timeout_in_secs) as resp:
            if parse_json:
                return json.load(resp)
            return resp.read().decode('utf-8')
    except urllib.request.HTTPError as error:
        print(error.file.read().decode('utf8'))
        raise
headers = {'Content-Type': 'application/json; charset=utf-8'}
data = json.dumps(payload).encode('utf-8')
urllib.request.urlopen(urllib.request.Request(url, method='PUT', headers=headers, data=data),
                       context=ssl._create_unverified_context())
wget # equivalent lib to the command-line tool

requests.post(form_url, data={'x':'42'})
    kennethreitz/grequests # Requests with Gevent to make asynchronous HTTP Requests easily
    aiohttp # for asyncio-based equivalent
    requests-futures # for asynchronous (non-blocking) HTTP requests
    txrequests # Twistted asynchronous requests
    httpx # async (both fully or under the hood with a sync frontend) HTTP 1.1 & 2 client with a similar API to requests
    requests_toolbet # multipart/form-data Encoder - User-Agent constructor - SSLAdapter - cookies/ForgetfulCookieJar
    requests-cache
    requests-respectful # requests capping
    requests-jwt # auth = JWTAuth(secret, alg='HS512', header_format='Bearer %s') - usage example: https://github.com/shaarli/python-shaarli-client/blob/master/shaarli_client/client/v1.py#L205
    cloudscraper # bypass Cloudflare's anti-bot page
    requests.packages.urllib3.util.retry # can retry on connect/read/all failures, cf. https://www.peterbe.com/plog/best-practice-with-retries-with-requests
        if retries:
            adapter = HTTPAdapter(max_retries=Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor))
            session.mount('http://', adapter)
            session.mount('https://', adapter)
connect timeout / read timeout / download size limit : https://web.archive.org/web/20231130143329/https://benbernardblog.com/the-case-of-the-mysterious-python-crash/
def requests_get_with_max_size(url):
    with closing(requests.get(url, stream=True, timeout=TIMEOUT)) as response:
        response.raise_for_status()
        content = ''
        for chunk in response.iter_content(chunk_size=GET_CHUNK_SIZE, decode_unicode=True):
            content += chunk if response.encoding else chunk.decode()
            if len(content) >= MAX_RESPONSE_LENGTH:
                raise RuntimeError("The response was too large (greater than {0} bytes).".format(MAX_RESPONSE_LENGTH))
        return content, response.headers
session.post(url, files={'upload': ('filename', file_to_upload, 'application/javascript')},
                  data={'action': 'upload', 'target': '/test/'}).raise_for_status()
response = requests.get(url, headers={"Client-IP":ip, "User-Agent": ua}, allow_redirects=true, stream=True)  # WARNING on POST params usage: json= != data=
if 400 <= response.status_code < 600:
    raise requests.HTTPError(str(response.status_code) + '\n' + response.text)
status_string = requests.status_codes._codes[404][0]; status_string = ' '.join(w.capitalize() for w in status_string.split('_')) # Alt: httplib.responses, cf. HTTP_STATUS_LINES in Bottle code: http://bottlepy.org/docs/dev/bottle.py
def passthrough_http_proxy(http_proxy, real_request_url):
    proxy_host, proxy_port = http_proxy.split(':')
    class HTTPProxyAdapter(requests.adapters.HTTPAdapter):
        def request_url(self, request, _):
            return request.url # use the FULL url of the resource to build the request line, instead of only its relative path
    def custom_parse_url(url):
        return requests.packages.urllib3.util.url.parse_url(url)._replace(host=proxy_host, port=proxy_port, scheme='http')
    with patch('requests.packages.urllib3.poolmanager.parse_url', new=custom_parse_url):
        session = requests.session()
        session.mount(scheme + '://', HTTPProxyAdapter())
        response = session.get(real_request_url)
        response.raise_for_status()
        return response.text
class HttpSession(requests.Session):
    'Allow to configure a timeout for all requests'
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop('timeout', None)
        super().__init__(*args, **kwargs)
    # Override: https://github.com/psf/requests/blob/v2.22.0/requests/sessions.py#L466
    def request(self, *args, **kwargs):
        if 'timeout' not in kwargs and self.timeout is not None:
            kwargs['timeout'] = self.timeout
        return super().request(*args, **kwargs)
class SessionWithPrefixUrl(requests.Session):
    # Recipe from: https://github.com/psf/requests/issues/2554#issuecomment-109341010
    def __init__(self, prefix_url):
        self.prefix_url = prefix_url
        super().__init__()
    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        return super().request(method, url, *args, **kwargs)
http_session = HttpSession(timeout=5)
http_session.mount('https://', HTTPAdapter(max_retries=3))
http_session.headers['User-Agent'] = USER_AGENT
http_session.verify = False
from http.client import HTTPConnection
HTTPConnection.debuglevel = 2  # enable verbose HTTP calls details on stdout for Python 3
responses/httmock # a mocking library for requests - Alt: getsentry/responses
betamaxpy/betamax # VCR/Wiremock-like HTTP mock: record & replay requests - cf. also: kevin1024/vcrpy
HTTPretty # Testing HTTP requests without any server, acting at socket-level
ariebovenberg/snug # organize your HTTP client code to ease reuse, async compatibility & tests
python-mocket # socket mocks

spiderclub/haipproxy # IP proxy pool, powered by Scrapy and Redis
community-libs/vaurien # TCP proxy to simulate chaos between your application and a backend server - Originated at Mozilla, not much maintained - Alt: Shopify/toxiproxy in Ruby ; kffl/speedbump in Go
st = speedtest.Speedtest() # speedtest-cli - provides download/upload speed based on speedtest.net

ramses # API generation framework: based on RAML, ElasticSearch & Pyramid -> https://realpython.com/blog/python/create-a-rest-api-in-minutes-with-pyramid-and-ramses/ & https://www.elastic.co/blog/make-an-elasticsearch-powered-rest-api-for-any-data-with-ramses
Kinto # minimalist JSON storage service, easy to bootstrap with Heroku/Docker, by Mozilla: https://kinto.readthedocs.io/en/stable/tutorials/install.html

aws/chalice # serverless microframework for AWS (API Gateway + Lambda) - provides: CLI for creating, deploying, and managing your app / an API to declare routes & views / automatic IAM policy generation
awslabs/aws-lambda-powertools-python # utilities for AWS Lambda functions to ease adopting best practices such as tracing, structured logging, custom metrics, and more

# Web frameworks (from barcamp@AFPY):
bottle # include server, only 1 file long, behind 0bin
CherryPy # good prod WSGI server, very easy to launch - Alt: bjoern > meinheld > gunicorn > uwsgi (in terms of perfs)
Eyepea/API-Hour # perf-oriented web APIs using AsyncIO & ujson - Alt: Sanic + uvloop, a fast drop-in replacement for asyncio ; squeaky-pl/japronto, "screaming-fast" & based on uvloop and picohttpparser
nameko # framework for building microservices: RPC/pub-sub over AMQP, websocket RPC and subscriptions
featherweight # transform functions into REST web services
Tornado # asynchronous web framework - can be used as a WSGI app with some limitations: http://www.tornadoweb.org/en/stable/guide/running.html#wsgi-and-google-app-engine
Falcon, flask-restful # to build HTTP APIs - not asynchronous and uses a thread-local context - note that Flask has many global variables & is not thread safe (for async)
hug # Flask alt based on Falcon, which provides auto documentation, input validation, type-handling with annotations and automatic versions
FastAPI # ReDoc & SwaggerUI + Pydantic + sStarlette = an async Flask alt which supports WebSocket & GraphQL
Flask(__name__, static_folder='..', static_url_path='', template_folder='.') # huge tuto: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
    flasgger # Swagger API for flask
    Flask-Caching
    flask-sqlalchemy
    flask-admin # admin interface on top of an existing data model
    flask-babel # adds i18n and l10n support
    flask-login # user session management
    Flask-HTTPAuth # Basic, Digest and Token HTTP authentication
    flask_weasyprint # easily provides a PDF export of an HTML page using Weasyprint
    mjhea0/awesome-flask # A curated list of awesome things related to Flask
    Talisman / Secure.py # add HTTP headers protecting against common webapps security issues
Quart # like Flask, but async -> ASGI - ~3x faster than Flask - cf. https://www.metal3d.org/blog/2020/de-flask-%C3%A0-quart/
reddit/baseplate # library to build web services on: includes metrics, tracing, logging, configuration parsing and gevent-based Thrift and WSGI servers meant to run under Einhorn
Django # cf. dedicated section
pyramid # more modular alternative to Django (= Pylons project)
+ web.py # very old now, written by Aaron Swarz, used by Yandex

python -m SimpleHTTPServer 8080 # --version > 3: -m http.server
gunicorn --reload # auto-restart on files changes - Python WSGI server
Uvicorn # lightning-fast ASGI server implementation, using uvloop and httptools
tiangolo/meinheld-gunicorn-flask-docker # Docker image with Meinheld managed by Gunicorn for high-performance web applications in Flask using Python 3, with performance auto-tuning - Alt: tiangolo/uvicorn-gunicorn-docker

WTForms # forms validation

pyswagger # generates a Python client from a JSON formatted Swagger (Open API) schema - Alt: Azure/autorest

# Flask tricks:
app.logger.addHandler(file_handler)
@app.errorhandler(404) # or 500
def internal_error(exception):
    app.logger.exception("Error 404: %r", {k:getattr(exception, k) for k in dir(exception)})
    raise_chained(exception, 'Error 500: ') # In Python 3: raise XYZ from exception
app.config.update({  # Loading configuration from env variables:
    'DB_PORT': int(os.environ.get('DB_PORT', Config.DB_PORT))
})
catch-all URL: http://flask.pocoo.org/snippets/57/
using Dependency Injector with Flask blueprints: https://python-dependency-injector.ets-labs.org/examples/flask-blueprints.html

def application(env, start_response): # Most basic native WSGI app
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['Hello World!'.encode('ascii')]
if __name__ == '__main__': # to launch a small WSGI server directly, without uwsgi / gunicorn / etc.
    from wsgiref.simple_server import make_server
    make_server('localhost', 8088, application).serve_forever()

saimn/sigal # simple static gallery generator like MinigalNano /files.gallery: https://chezsoi.org/shaarli/shaare/k7TT8Q

jstasiak/python-zeroconf  # multicast DNS service discovery - usage example: nils-werner/zget filename-based peer to peer file transfer
pycares # asynchronous DNS resolution
octodns # manage DNS across multiple providers with config versioning

locust # user load testing simulating millions of simultaneous users : Alt: ab (Apache Benchmarking), tarekziade/boom, wg/wrk
mininet # realistic virtual network, running real kernel, switch and application code, on a single machine
ipaddr, netaddr > socket.inet_aton # string IP to 32bits IP + validate IP, !! '192.168' is valid
IPy(ipsrc).iptype() == 'PRIVATE' # check ranges 10.0.0.0–10.255.255.255, 172.16.0.0–172.31.255.255 & 192.168.0.0–192.168.255.255
scapy # packet injection/manipulation for many network protocols - Alt: dpkt, can read .pcap files
pystack # create modifiable TCP/IP stacks, based on scapy & netfilter
pypcap # catpure network traffic
kevin1024/vcrpy # record / replay HTTP interactions - cf. also betamaxpy/betamax
impacket # programmatic access to the packets and for some protocols: IP, TCP, UDP, ICMP, IGMP, ARP, NMB, DCE/RPC, SMB1-3 and MS-DCERPC
py2bpf # Python to Berkeley Packet Filter bytecode converter
wifi # wrapper around iwlist and /etc/network/interfaces
kootenpv/access_points # scan your WiFi and get access point information and signal quality
tn = telnetlib.Telnet('example.com')
tn.read_until("login: ")
tn.write(user + "\n")

Brython.info # replace Javascript as the scripting language for the Web
Pyodide # Python with the scientific stack, compiled to WebAssembly
Skulpt # entirely in-browser implementation of Python, by compiling it to Javascript

yandex/gixy # a tool to analyze Nginx configuration. The main goal of Gixy is to prevent security misconfiguration and automate flaw detection.


"""""""""""""
"" Hosting ""
"""""""""""""
zappa # serverless framework for AWS lambda / API Gateway
foxmask/shaarpy # Shaarli in Django
cloudtools/troposphere # create AWS CloudFormation descriptions in JSON from code
heroku
pythonanywhere.com


"""""""""""""""""""""""""
"" Hacking & Forensic  ""
"""""""""""""""""""""""""
danmcinerney/wifijammer # How to kick everyone around you off wifi with python
Patator # Multi-threaded Service & URL Brute Forcing Tool

pywin32 # Windows API, e.g. win32crypt.CryptUnprotectData - cf. http://docs.activestate.com/activepython/2.6/pywin32/PyWin32.HTML / http://timgolden.me.uk/pywin32-docs/PyWin32.html
    excel = win32.gencache.EnsureDispatch('Excel.Application'); excel.Visible = True
    outlook = win32.gencache.EnsureDispatch('Outlook.Application'); new_mail = outlook.CreateItem(0)
    win10toast # create Windows 10 notifications
theller/comtypes # access and implement both custom and dispatch based COM interfaces
n1nj4sec/memorpy # search/edit Windows programs memory

Gallopsled/pwntools # CTF framework and exploit development library
angr # binary analysis platform

# Violent Python: A Cookbook for Hackers, Forensic Analysts, Penetration Testers and Security Engineers
python-nmap # port scanner
winreg # access to the Windows registry


"""""""""""""
"" Django
"""""""""""""
# template engine 0/20 (should be replaceable soon) / ORM++, as good as SQLAlchemy but more high-level
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
# Alt: Whitenoise

AppConfig.ready() # to perform initialization tasks (such as registering signals); called as soon as the registry is fully populated; !! AVOID INTERACTING WITH THE DB !! -> use migrations and e.g. RunPython to populate the DB with initial data

django-rest-framework
django.utils.translation # i18n -> very good intro & tips: https://speakerdeck.com/pycon2015/sarina-canelake-i18n-world-domination-the-easy-way
django-expiry # Expiry rules for Django sessions

djangocolors_formatter.py # one-file recipe
django-debug-toolbar
django-toolbelt

Tastypie # webservice framework to create REST-style APIs, e.g. for an autocompletion service
factoryboy # > fixtures for DB testing (personnal opinion: several fixtures can sometimes be simpler AND avoid dangerous over-mocking) - Alt: mixer
pifpaf # suite of fixtures and a CLI tool that allows to start and stop daemons for a quick throw-away usage - supports: PostgreSQL, MySQL, memcached, InfluxDB, etcd, Redis, Elasticsearch, Zookeeper, Gnocchi, Aodh, Ceph, RabbitMQ, FakeS3, Consul, Keystone, CouchDB, S3rver, MongoDB, OpenStack Swift, Vault

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

import logging as l
lg = l.getLogger('django.db.backends')
lg.setLevel(l.DEBUG)
lg.addHandler(l.StreamHandler()) # Pour que le SQL de tous vos appels à la BDD soient affichés dans le terminal


"""""""""""""""""""""""""
"" Other libs & tools
"""""""""""""""""""""""""
fmoo/python-editor # programmatically open a text editor, captures the result

webbrowser.open_new_tab # Firefox/Opera/Chrome instrumentation
mozilla/gecko-dev/testing/marionette/client # remotely control a Gecko-based browser running a Marionette server - https://marionette-client.readthedocs.io
SeleniumHQ/selenium/py # browser automation, can be combined with geckodriver for Firefox - http://selenium-python.readthedocs.io
pyautogui # send virtual keypresses and mouse clicks to the OS - cf. chapt 18 of AutomateTheBoringStuff
sikuli # Java-based (with JS, Python & Ruby ports) visual workflow, able to identify images on screen using OpenCV
pyhooked # pure Python hotkey hook: react on specific mouse/keyboard events
boppreh/keyboard # hook and simulate global keyboard events on Windows and Linux

watchdog # inc. cmd watchmedo -> monitor/observe files changes - FROM: S&M - not Cygwin-friendly due to ctypes.wintypes usage
livereload # browser automatic reloading for development - Alt: hupper for reloading server code

filemagic, ahupp/python-magic # interfaces to libmagic file type identification, aka the "file" command under Unix : it identifies file types by checking their headers according to a predefined list of file types - Alt: commit/identify

reload(module) # Python 2 only, else : importlib.reload - Alt: xreload
modulefinder # determine the set of modules imported by a script

asynchat, irc, sleekxmpp, embolalia/willie # IRC/XMPP bots
mailr, mailbox, imaplib, smtpd, smptplib, kootenpv/yagmail # for emails, cf. ascii_art_email.py
Miksus/red-mail  # makes sending emails trivial and has advanced features such as: Attachments, Templating (with Jinja), Embedded images, Prettified tables, Send as cc or bcc, Gmail preconfigured
modoboa # email hosting made simple, with webUI + amavis + monitoring, for postfix & dovecot
gmvault # Gmail backup CLI
paramiko # remote SSH/SFTP connexion

scales # metrics for Python, send data points to Graphite - Pros: inc. with-context to measure latency, metering-rates 1/5/15min, PmfStat => stdev, p99 - Cons: not actively maintained, its code uses lots of global state, there is test code in its source, a thread launched at import time and its documentation is incomplete

@retry # https://github.com/rholder/retrying - Exponential Backoff algorithm implementation: deprecated! => tenacity - Alt: tenacity

daviddrysdale/python-phonenumbers # port of Google's libphonenumber to validate phone numbers
TwilioLookupsClient().phone_numbers.get("15108675309", include_carrier_info=True) # Twilio API phone number validation

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

from getpass import getpass # get password without echoing it
hmac, hashlib.md5('string').hexdigest()
dwolfhub/zxcvbn-python # password strength estimation
from cryptography.fernet import Fernet # symmetric encryption
jake-jake-jake/historical_ciphers # Caesar, Transposition and Affine ciphers
mitsuhiko/itsdangerous # helpers to pass trusted data to untrusted environments by signing content, e.g. serialize and sign a user ID
import bcrypt, hmac; hashed = bcrypt.hashpw(password, bcrypt.gensalt()) # Secure Password Storage in 2016
if (hmac.compare_digest(bcrypt.hashpw(password, hashed), hashed)): ...  # Login successful
hmac.compare_digest(a, b) # String equality check that prevent timing analysis
jaraco/keyring # access the system keyring service, so that you can set_password / get_password - Support: Mac OS X Keychain, Freedesktop Secret Service (requires secretstorage), KWallet (requires dbus), Windows Credential Vault

ConfigParser, configobj # std configuration files format
csvkit > csv (csv.DictReader >handier> csv.reader), xlwt, xlrd, openpyxl < tablib # generic wrapper around all those. Also: pyxll to write Excel addins & macros in Python, csvx, pylightxl
writer = csvkit.writer(sys.stdout)
with open(sys.argv[1]) as csv_file:
    for row in csvkit.reader(csv_file):
        writer.writerow(row)
harelba/q  # run SQL directly on CSV or TSV files
aspy.yaml, yaml # !!! yaml.load() is an unsafe operation ! Use yaml.safe_load() - Also: beware the inconsistent behaviours: http://pyyaml.org/ticket/355
# How to load/dump YAML and convert tagged nodes to almost-native types: https://death.andgravity.com/any-yaml
ruamel # YAML parser / writer with support for roundtrip comments
def extract_comments_from_yaml_ordereddict(d):
    for pair in d.ca.items.values():
        for comment_token in pair[1]:
            yield comment_token.value
imbal/safeyaml # a linter for YAML as an aggressively small subset of YAML
toml # TOML parser - Alt: TOML Kit, a parser that preserves all comments, indentations, whitespace and internal element ordering
iniconfig # .ini file parser
cPickle # binary format, generic, fast & lighweight - DO NOT USE IT ! -> "untrusted pickles can execute arbitrary Python code" + "you can’t even easily tell which classes are baked forever into your pickles" -> Alt: eeve/camel PyYaml-based serialization (inc. versionning & use YAML metadata)
# + PyCloud make it possible to pickle functions dependencies
marshmallow #, ORM/ODM validate input data against schemas + serialize or deserialize data from/into primitive Python types

lz4, bz2, gzip, tarfile, zlib.compress(string), mitsuhiko/unp # to unpack any archive
archive = zipfile.ZipFile('foo.zip', mode='w')
for root, dirs, files in os.walk('/path/to/foo'): # path.py walkfiles() is even better to crawl a directory tree / files hierarchy - And benhoyt/scandir is faster and now in the Python 3.5 stdlib
    for name in files:
        archive.write(os.path.join(root, name), compress_type=zipfile.ZIP_DEFLATED)

pygeoip, mitsuhiko/python-geoip, python-geoip@code.google, maxmind/geoip-api-python, pierrrrrrre/PyGeoIpMap # this latest one provide a useful command-line tool
OpenTransitTools/gtfsdb # GTFS (General Transit Feed Specification) DB : public transportation schedules and associated geographic information

pyusb  # interfaces to FTDI D2XX drivers to manipulate USB devices


"""""""""""""
"" Architecture
"""""""""""""
Clean Architecture by Leonardo Giordani: inspired by Robert Martin ideas (and to me, very close to an hexagonal architecture)
- layered & spherical: it has inner layers encompassed by outer ones, the former being oblivious of the existence of the latter
- the deeper a layer is, the more abstract & buisness-oriented it is
- Talk inwards with simple structures, talk outwards through interfaces
- main layers:
  * Entities: lightweight domain models
  * Use cases: as small a possible
  * External systems: HTTP API, database...


"""""""""""""
"" Ansible
"""""""""""""
pip install "ansible-lint[yamllint]" && ansible-lint
ansible-galaxy install -r requirements.yml
ansible-playbook -i inventory_remote.py --extra-vars "ansible_sudo_pass=$ORKA_PASSWORD" -t playbook-name main.yml -vv
ansible-community/molecule # playbook testing with multiple instances, operating systems and distributions, virtualization providers, test frameworks and testing scenarios
mitogen-hq/mitogen # execute Ansible playbooks in a more efficient way (decreases the execution time)

# Enable strict / fail-fast mode:
any_errors_fatal: true

# Enable task execution time profiling in ansible.cfg:
[defaults]
callback_whitelist = ansible.posix.profile_tasks

- name: Get new VM IP & port
  shell: ./inventory_remote.py
  register: inventory_remote

- set_fact:
    inventory: "{{ inventory_remote.stdout | from_json }}"

- name: Wait for VM to accept SSH connexions
  with_dict: "{{ inventory._meta.hostvars }}"
  wait_for:
    host: "{{ item.key }}"
    port: "{{ item.value.ansible_port }}"
    timeout: 60


"""""""
"" Fun
"""""""
for ...:
else:  # Awkward loop construct (also exist: try/except/else)

from __future__ import braces

import this
import antigravity

a='a=%s;print a%%`a`';print a%`a` # Quine

PEP 712 - Proposal to make unittest2 more accurate: FFFFFFFUUUUUUUUUUUUUUUUUCK

menu = ordereddict[ # hack to create an OrderedDict constructor - cf. http://stackoverflow.com/a/37259917/636849 & odictliteral package
   "about" : about,
   "login" : login,
   'signup': signup
]


"""""""""""""
"" Python 3
"""""""""""""
asottile/pyupgrade # A tool (and pre-commit hook) to automatically upgrade syntax for newer versions of the language.

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
pyre-check # annotation-based type checker

b'I am an immutable basic byte array of type "bytes"'
bytearray(b"I am mutable")

__bytes__() and __str__()

nonlocal

first, *rest, last = range(5) # extended iterable unpacking

try:
    v = {}['a']
except KeyError as e:
    raise ValueError('failed') from e # exception chaining - In Python 2: from future.utils import raise_from - Also available in pkg six

with concurrent.futures.ProcessPoolExecutor() as executor: # Asynchronous
    processed_args = list(executor.map(big_calculation, args)) # faster than without 'executor'
    futures = {executor.submit(other_big_calc, arg) for arg in processed_args}
    for future in as_completed(futures):
        if future.exception():
            raise future.exception()
        yield future.result()
wait(futures, return_when=FIRST_EXCEPTION)  # cf. http://masnun.com/2016/03/29/python-a-quick-introduction-to-the-concurrent-futures-module.html

yield from iterator # delegate

def foo(a, b, *, keyword=None): pass # keywords-only functions arguments

class MyClass: pass # no need to inherits from object

class Metaaa(metaclass=MyClass): pass # no more __metaclass__ attribute

super() # new simpler syntax !

obj.__qualname__

from enum import Enum, IntEnum  # A very nice recipe: CoerciveEnum - https://github.com/PyFPDF/fpdf2/blob/master/fpdf/enums.py

from functools import \
        singledispatch, \ @foo.register(int) def _(obj, verbose=False): ...
    total_ordering, # to define all comparison methods given __eq__ and __lt__, __le__, __gt__, or __ge__
    lru_cache # memoize / cache for pure functions - avoid using it as a decorator so that the cache is local and not module-global - has a .cache_info() function that returns a named tuple showing hits, misses, maxsize and currsize
    # Alt: Py2.7 decorator recipe for caching with TTL : https://wiki.python.org/moin/PythonDecoratorLibrary#Cached_Properties
    # Alt: pypi/cached-property / boltons.cacheutils.LRI / boltons.cacheutils.LRU

collections.ChainMap({}, d1, d2) # view of multiple dicts - Hidden Py2.7 backport: from ConfigParser import _Chainmap as ChainMap - Alt: Py2ChainMap

from pathlib import Path # e.g. Path('/etc') / 'init.d' / 'reboot'
def walk_files(directory, only=None):
    for dirpath, _, filenames in os.walk(directory):
        dirpath = Path(dirpath)
        if not only or only == 'directories':
            yield dirpath.resolve()
        if not only or (only == 'files'):
            for filename in filenames:
                yield (dirpath / filename).resolve()


#------------------------------------------------------------------------------
# Python 3.3

types.MappingProxyType # read-only dict : https://github.com/topper-123/Articles/blob/master/New-interesting-data-types-in-Python3.rst


#------------------------------------------------------------------------------
# Python 3.5

# PEP448 : unpacking generalized
l = (1, *[2])
d = {"j": 9, **{"i": 8}}

async def foo(): ...
uvloop  # drop-in replacement for asyncio event loop, written in Cython & 2x faster than NodeJS

python -m zipapp my_project_dir  # generates a .pyz

subprocess.run > check_call


#------------------------------------------------------------------------------
# Python 3.6
f-strings
subclassable typing.NamedTuple


#------------------------------------------------------------------------------
# Python 3.7 - cf. http://sametmax.com/python-3-7-sort-de-sa-coquille/
from dataclasses import asdict, astuple, dataclass, replace
@dataclass(repr=True, eq=True, order=True, frozen=True)
class Achat:
    produit: str
    prix: float
    quantite: int = 0

namedtuple # supporte les valeurs par défaut

python -X dev
python -X importtime

breakpoint() # alias pour: import pdb; pdb.set_trace()

dict # now ensured to be ordered

importlib.resources # replace pkg_resource

contextlib.nullcontext # noop context manager


#-----------
# Python 3.8
functools.cached_property

f'{expr=}'  # expand to the text of the expression, an equal sign, then the representation of the evaluated expression

if (n := len(a)) > 10:  # Assignment expressions

def f(a, b, /, c, d, *, e, f):  # Positional-only parameters

from importlib.metadata import version, requires, files
version('requests')  # '2.22.0'
list(requires('requests'))  # ['chardet (<3.1.0,>=3.0.2)']
list(files('requests'))[:5]

asyncio.run()  # is now stable API

sys.addaudithook() # allows to watch many events + can be used to forbid networks connections in a secure way
# https://docs.python.org/3/library/audit_events.html#audit-events
# https://www.reddit.com/r/Python/comments/vjlfom/comment/idnwhfx/?context=3


#-----------
# Python 3.9
{"a": 1} | {"a": 2}  # dict union. Also: |=

str.removeprefix(prefix) and str.removesuffix(suffix)  # new methods

zoneinfo  # new builtin module providing IANA time zones like Pypi tzdata package used to do

+ speed improvements


#-----------
# Python 3.10

PYTHONWARNDEFAULTENCODING : raise EncodingWarning when no encoding was specified when opening text files

match event.get():  # pattern matching - Horrible uses: https://www.hillelwayne.com/post/python-abc/
    case Click(position=(x, y)):
        handle_click_at(x, y)


#-----------
# Python 3.11

tomllib: Support for Parsing TOML in the Standard Library

try:
    ...
except* SpamError:
    ...
except* FooError as e:
    ...
except* (BarError, BazError) as e:
    ...

asyncio.TaskGroup


#-----------
# Python 3.12
with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
    fp.write(b'Hello world!')
    fp.close()
    # the file is closed, but not removed
