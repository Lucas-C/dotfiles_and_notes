import gc
from contextlib import contextmanager
from functools import wraps
from time import perf_counter  # used by timeit module

def trace_exec_time(what, *args, **kwargs):
    """
    Inspired by the following:
    - timeit.Timer.timeit
    - http://dabeaz.blogspot.it/2010/02/function-that-works-as-context-manager.html
    - http://code.activestate.com/recipes/577896/
    """
    @contextmanager
    def benchmark(name, *args, **kwargs):
        gc_was_enabled = gc.isenabled()
        gc.disable()
        start = perf_counter()
        yield
        end = perf_counter()
        if gc_was_enabled:
            gc.enable()
        print(name, args, kwargs, "%0.3fs" % (end - start))
    if hasattr(what,"__call__"):
        @wraps(what)  # Alt: wrapt.decorator
        def wrapper(*args, **kwargs):
            with benchmark(what.__name__, *args, **kwargs):
                return what(*args, **kwargs)
        return wrapper
    else:
        return benchmark(what, *args, **kwargs)

