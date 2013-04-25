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
