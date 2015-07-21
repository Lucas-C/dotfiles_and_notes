# Call PDB when an exception is raised
# It tries to use 'gotcha/ipdb' if available, to benefit from IPython PDB
# Neither of them will work INSIDE IPython as it also redefines sys.excepthook
# USAGE:
#   python -m pdb_on_err script.py arg1 arg2
#   python -m pdb_on_err -c 'import sys; print sys.argv[0]' 0
#   from pdb_on_err import launch_pdb_on_exception # to invoke manually as a 'with' context block
# FROM: http://stackoverflow.com/questions/242485/starting-python-debugger-automatically-on-error
from imp import find_module
import os, sys

def ret_except(func, *args, **kwargs):
    """
    Utility function useful in pdb to catch exceptions in a variable.
    :returns: an :class:`Exception` if any is raised during the call, else the normal function return value
    """
    try:
        return func(*args, **kwargs)
    except Exception as err:
        return err

try:
    from ipdb import launch_ipdb_on_exception as launch_pdb_on_exception
except ImportError:
    import contextlib
    import pdb, traceback

    @contextlib.contextmanager
    def launch_pdb_on_exception():
        ps1_before = getattr(sys, 'ps1', None)
        if ps1_before:
            delattr(sys, 'ps1')
        excepthook_before = sys.excepthook
        sys.excepthook = pdb_excepthook
        yield
        sys.excepthook = excepthook_before
        if ps1_before:
            setattr(sys, 'ps1', ps1_before)

    def pdb_excepthook(type, value, tb):
        # do nothing if we are in interactive mode or we don't have a tty-like device
        if not hasattr(sys, 'ps1') and sys.stderr.isatty():
            # print the exception...
            traceback.print_exception(type, value, tb)
            print
            # ...then start the debugger in post-mortem mode.
            pdb.post_mortem(tb)
        sys.__excepthook__(type, value, tb)

def main():
    prog_name = sys.argv.pop(0)
    cmdstr = get_arg_value_if_next(sys.argv, '-c')
    if cmdstr:
        exec(cmdstr)
        return
    modname = get_arg_value_if_next(sys.argv, '-m')
    if modname:
        filename = find_module(modname)[1]
        if os.path.isdir(filename):
            filename = os.path.join(filename, '__main__.py')
    else:
        filename = sys.argv[0]
    with open(filename) as open_file:
        code = compile(open_file.read(), filename, 'exec')
        exec(code, {'__name__':'__main__', '__file__':filename})

def get_arg_value_if_next(argv, flag):
    try:
        c_flag_index = argv.index(flag)
    except ValueError:
        return
    del argv[c_flag_index]
    return argv.pop(c_flag_index)

if __name__ == '__main__':
    with launch_pdb_on_exception():
        main()

