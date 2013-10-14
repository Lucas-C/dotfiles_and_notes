# Call PDB when an exception is raised
# USAGE:
#   python -m pdb_on_err script.py arg1 arg2
#   python -m pdb_on_err -c 'import sys; print sys.argv[0]' 0
# FROM: http://stackoverflow.com/questions/242485/starting-python-debugger-automatically-on-error
from imp import find_module
from os import path
import sys
import traceback, pdbi

def excepthook(type, value, tb):
    # do nothing if we are in interactive mode or we don't have a tty-like device
    if not hasattr(sys, 'ps1') and sys.stderr.isatty():
        # print the exception...
        traceback.print_exception(type, value, tb)
        print
        # ...then start the debugger in post-mortem mode.
        pdbi.post_mortem(tb)
    sys.__excepthook__(type, value, tb)

sys.excepthook = excepthook


def next_arg_is(flag):
    try:
        c_flag_index = sys.argv.index(flag)
        del sys.argv[c_flag_index]
        arg = sys.argv[c_flag_index]
        del sys.argv[c_flag_index]
        return arg
    except ValueError:
        pass

def main():
    sys.argv = sys.argv[1:]
    cmdstr = next_arg_is('-c')
    if cmdstr:
        exec(cmdstr)
        return
    modname = next_arg_is('-m')
    if modname:
        filename = find_module(modname)[1]
    else:
        filename = sys.argv[0]
    execfile(filename, {'__name__':'__main__', '__file__':filename})

if __name__ == '__main__':
    main()
