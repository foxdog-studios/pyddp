from functools import wraps
from threading import Condition

from ddp.timeout import wrap_timeout


def with_condition(method):
    @wraps(method)
    def wrapper(future, *args, **kwargs):
        with future._cond:
            return method(future, *args, **kwargs)
    return wrapper


class Future:
    def __init__(self):
        self._callbacks = []
        self._cond = Condition()
        self._is_set = False
        self._result = None

    def __bool__(self):
        return self.is_set()

    def _call_callback(self):
        for callback in self._callbacks:
            callback(self._result)
        # Prevent memory leak
        self._callbacks = None

    @with_condition
    def add_callback(self, callback):
        if self._is_set:
            callback(self._result)
        else:
            self._callbacks.append(callback)

    @with_condition
    def is_set(self):
        '''
        Is the result set?

        This may block for a short period of time.
        '''
        return self._is_set

    @wrap_timeout
    @with_condition
    def get(self, timeout=None):
        '''
        Get the result.

        This blocks util the result is set. If `timeout` is given,
        this will block for at most `timeout` milliseconds.
        '''
        while not self._is_set:
            self._cond.wait(timeout=timeout())
        return self._result

    @with_condition
    def set(self, result):
        '''
        Set the value and notify waiting threads.

        This may block for a short period of time.
        '''
        if self._is_set:
            raise ValueError('result is already set')
        self._is_set = True
        self._result = result
        self._call_callback()
        self._cond.notify_all()


class CompositeFuture():
    def __init__(self, futures):
        self._futures = futures

    def __bool__(self):
        return self.is_set()

    def __len__(self):
        return len(self._futures)

    def __getitem__(self, i):
        return self._futures[i]

    def is_set(self):
        return all(self._futures)

    @wrap_timeout
    def get(self, timeout=None):
        return [future.get(timeout=timeout) for future in self._futures]

