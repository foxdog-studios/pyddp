from functools import wraps
from numbers import Number
import time


def timeout(seconds):
    start = time.time()
    while True:
        remaining = seconds - (time.time() - start)
        if remaining <= 0:
            raise RuntimeError()
        yield remaining


def infinite_timeout():
    while True:
        yield None


def wrap_timeout(method):
    @wraps(method)
    def wrapper(future, *args, **kwargs):
        to = kwargs.get('timeout', None)
        if to is None:
            to = infinite_timeout().__next__
        elif isinstance(to, Number):
            to = timeout(to).__next__
        kwargs['timeout'] = to
        return method(future, *args, **kwargs)
    return wrapper

