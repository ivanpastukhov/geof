import functools
import time


def timeit(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ts = time.time()
            result = func(*args, **kwargs)
            te = time.time()
            runtime = te - ts
            logger.warning(f'takes {runtime} !')
            return result
        return wrapper
    return decorator

