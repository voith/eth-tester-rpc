"""
code copied from web3._utils.decorators
"""
import functools
import threading


def reject_recursive_repeats(to_wrap):
    """
    Prevent simple cycles by returning None when called recursively with same instance
    """
    to_wrap.__already_called = {}

    @functools.wraps(to_wrap)
    def wrapped(*args):
        arg_instances = tuple(map(id, args))
        thread_id = threading.get_ident()
        thread_local_args = (thread_id,) + arg_instances
        if thread_local_args in to_wrap.__already_called:
            raise ValueError('Recursively called %s with %r' % (to_wrap, args))
        to_wrap.__already_called[thread_local_args] = True
        try:
            wrapped_val = to_wrap(*args)
        finally:
            del to_wrap.__already_called[thread_local_args]
        return wrapped_val
    return wrapped
