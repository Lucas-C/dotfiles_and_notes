def raise_chained(err_caught, prefix_err_msg, custom_err_type=None):
    """
    Re-raise Python exception and preserve stack trace
    Create a new exception of the same type by passing a single message string as a parameter
    Thread-proof
    
    The following code is the simplest way to add informations to an exception:
        except Exception as err:
            err.args += 'More_infos', # tuple
            raise
    But some exceptions redefine __str__, and additional arguments won't be displayed (e.g. urllib2URLError)
    This function is an alternative solution
    """
    import sys
    err_cls = custom_err_type or type(err_caught)
    traceback = sys.exc_info()[2]
    raise err_cls, err_cls(prefix_err_msg + str(err_caught.message)), traceback

