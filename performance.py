from collections import defaultdict
import time


function_timings = defaultdict(list)

def timer_decorator(func) -> None:
    def timer_wrapper(*args, **kwargs):
        func_name = func.__name__
        start_time = time.time()
        ret_val = func(*args, **kwargs)
        func_time = time.time() - start_time
        function_timings[func_name].append(func_time)
        return ret_val
    return timer_wrapper