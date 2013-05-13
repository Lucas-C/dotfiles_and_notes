def _set_trace():
    """
    Wrapper for IPython debugger.
    If not available, fallback to classic pdb

    Usage : import ipdb; ipdb.set_trace()
    """
    try:
        from IPython.core.debugger import Pdb
        return Pdb().set_trace
    except ImportError:
        import pdb
        return pdb.set_trace

set_trace = _set_trace()

