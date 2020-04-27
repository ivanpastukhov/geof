import functools
import time


def timeit(logger):
    print('logger is called!')
    def decorator(func):
        print('gonna decorate')
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print('now wrapped')
            ts = time.time()
            result = func(*args, **kwargs)
            te = time.time()
            runtime = te - ts
            logger.debug(f'takes {runtime} !')
            logger.warning('AAAAAAAAA!!!!!!!')
            return result
        return wrapper
    return decorator

