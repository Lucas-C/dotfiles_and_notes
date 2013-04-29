"""""""""""
"" Python
"""""""""""

# AWESOME for scripting
http://amoffat.github.io/sh/

# HTTP server
python -m SimpleHTTPServer 8080 # --version > 3: -m http.server

__slots__ # attribute
# Its proper use is "to save space in objects. Instead of having a dynamic dict that allows adding attributes to objects at anytime, there is a static structure which does not allow additions after creation. This saves the overhead of one dict for every object that uses slots."

# get exec time
python -mtimeit -s'xs=range(10)' '[hex(x) for x in xs]' # or 'map(hex, xs)'

# DO NOT use other default parameter values than None
def foo(x = []):
    x.append('do')
    return x
# + initialization is static

foo()
foo()

# __repr__ : unambigous, as possible 'eval'uable
"MyClass(this=%r,that=%r)" % (self.this,self.that)

# Funny loop construct
for ...:
    break
else:

# datetime.utc_now() better than time.time()

__all__ = ['bar', 'foo']
# list of symbol to export from module. Default: all symbol not starting with _

__call__
# if a = A(), this is the method called when doing a()

Foo = type('Foo', (object,), {'bar':True})
# on-the-fly class creation

# 'type' is the metaclass Python uses to create all classes behind the scenes
# aka, the most common __class__.__class__ of an object
# But you can specify your own __metaclass__ !

# PyCharm : code inspection
