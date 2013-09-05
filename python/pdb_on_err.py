# Call PDB when an exception is raised
# USAGE:
#   python -m pdb_on_err script.py arg1 arg2
#   python -m pdb_on_err -c 'import sys; print sys.argv[0]' 0
# FROM: http://stackoverflow.com/questions/242485/starting-python-debugger-automatically-on-error
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

if __name__ == '__main__':
    sys.argv = sys.argv[1:]
    try:
        c_flag_index = sys.argv.index('-c')
        del sys.argv[c_flag_index]
        command = sys.argv[c_flag_index]
        del sys.argv[c_flag_index]
        exec(command)
    except ValueError:
        execfile(sys.argv[0])

