import functools
import time


def timeit(logger):
    print('logger is called!')
    def decorator(func):
        print('gonna decorate')
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ts = time.time()
            result = func(*args, **kwargs)
            te = time.time()
            runtime = te - ts
            logger.debug(msg=f'takes {runtime} !')
            return result
        return wrapper
    return decorator

