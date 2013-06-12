# Other solution: http://www.anattatechnologies.com/q/2012/05/timeout-command-in-python/
from functools import wraps
from os import getpid, kill
from signal import getsignal, signal, SIG_DFL, SIG_IGN
from threading import current_thread, Thread
from time import sleep

_signals_in_use = set((SIG_IGN,))

class TimeoutException(Exception): pass

def call_with_timeout(timeout, timeout_signal, fn, *args, **kwargs):
    """
    Call a function but raise a TimeoutException if the timeout elapses.
    A previously registered signal handler for the signal given will be be kept but will be inactive during the call.
    This can NOT be used outside the main thread.
    Can be nested, as long as signals are not reused.

    Example:
        call_with_timeout(10, signal.SIGUSR1, my_function, {'list':[]}, x=42)

    :param timeout: a floating point number specifying the maximum number of seconds the function can take,
        e.g. datetime.timedelta.total_seconds()
    :param timeout_signal: the signal to send to the main thread to notify the timeout
    :param fn: any Python callable
    :param args: optional paramters
    :param kwargs: optional paramters
    """
    if current_thread().name != 'MainThread':
        raise Exception("Module {} functions can not be called outside the main thread".format(__name__))

    prev_hanlder = getsignal(timeout_signal)
    if not prev_hanlder in (SIG_DFL, SIG_IGN):
        raise Exception("A user-defined handler already exist for {}: {}".format(timeout_signal, prev_hanlder))

    global _signals_in_use
    if timeout_signal in _signals_in_use:
        raise Exception("Signal {} already in use".format(timeout_signal))
    _signals_in_use.add(timeout_signal)

    timeout_signal_exception = type('TimeoutException{!s}'.format(timeout_signal), (TimeoutException,), {})

    def signal_handler(signum, frame):
        signal(timeout_signal, prev_hanlder)
        global _signals_in_use
        if timeout_signal in _signals_in_use:
            raise timeout_signal_exception("Function {fn} called with args={args}, kwargs={kwargs} timed out after {timeout}s".format(
                fn=fn, args=args, kwargs=kwargs, timeout=timeout))

    signal(timeout_signal, signal_handler)

    def send_signal_after_timeout(pid, timeout, timeout_signal):
        sleep(timeout)
        kill(pid, timeout_signal)

    thread = Thread(target=send_signal_after_timeout, args=(getpid(), timeout, timeout_signal))
    thread.daemon = True
    thread.start()

    try:
        return fn(*args, **kwargs)
    finally:
        _signals_in_use.discard(timeout_signal)


def set_timeout(timeout, timeout_signal):
    """
    Decorator equivalent of 'call_with_timeout'.
    """
    def _set_timeout(fn):
        @wraps(fn)
        def wrapped_fn(*args, **kwargs):
            return call_with_timeout(timeout, timeout_signal, fn, *args, **kwargs)
        return wrapped_fn

    return _set_timeout


