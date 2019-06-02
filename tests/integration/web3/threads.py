"""
A minimal implementation of the various gevent APIs used within this codebase.
"""
import threading


class ThreadWithReturn(threading.Thread):
    def __init__(self, target=None, args=None, kwargs=None):
        super().__init__(
            target=target,
            args=args or tuple(),
            kwargs=kwargs or {},
        )
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self._return = self.target(*self.args, **self.kwargs)

    def get(self, timeout=None):
        self.join(timeout)
        try:
            return self._return
        except AttributeError:
            raise RuntimeError("Something went wrong.  No `_return` property was set")


def spawn(target, *args, thread_class=ThreadWithReturn, **kwargs):
    thread = thread_class(
        target=target,
        args=args,
        kwargs=kwargs,
    )
    thread.daemon = True
    thread.start()
    return thread
