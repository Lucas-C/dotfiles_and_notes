#FROM: http://stackoverflow.com/questions/242485/starting-python-debugger-automatically-on-error
import sys

def info(type, value, tb):
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
    # we are in interactive mode or we don't have a tty-like
    # device, so we call the default hook
        sys.__excepthook__(type, value, tb)
    else:
        import traceback, pdb
        # we are NOT in interactive mode, print the exception...
        traceback.print_exception(type, value, tb)
        print
        # ...then start the debugger in post-mortem mode.
        # pdb.pm() # deprecated
        pdb.post_mortem(tb) # more "modern"

sys.excepthook = info

if __name__ == '__main__': # so that it can used as 'python -m debug script.py arg1 arg2'
    sys.argv = sys.argv[1:]
    execfile(sys.argv[0])

