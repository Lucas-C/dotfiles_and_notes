"""
Wrapper for IPython debugger.
If not available, fallback to classic pdb

USAGE:  import pdbi; pdbi.set_trace()
OR:     import pdbi; pdbi.sh()
"""

class pdbi(object):
    def __init__(self):
        try:
            from IPython.core.debugger import Pdb
            self.pdb = Pdb()
        except ImportError:
            import pdb
            self.pdb = pdb

    def __getattr__(self, attr):
        print attr
        return getattr(self.pdb, attr)

    def sh(self):
        """
        http://ipython.org/ipython-doc/dev/interactive/reference.html#embedding
        """
        from IPython.frontend.terminal.embed import InteractiveShellEmbed
        from IPython.config.loader import Config
        import sys
        frame = sys._getframe().f_back
        msg = 'Stopped at {0.f_code.co_filename} and line {0.f_lineno}'.format(frame)
        InteractiveShellEmbed()(msg, stack_depth=2)


import sys
sys.modules[__name__] = pdbi()

