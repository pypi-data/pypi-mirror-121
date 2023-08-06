from functools import wraps

import pendulum

def timer(function):
    """
    Simple decorator to measure function execution time
    """
    @wraps(function)
    def function_wrapper():
        start = pendulum.now()
        function()
        elapsed_time = pendulum.now() - start
        print(f"Execution time - {elapsed_time.microseconds} ms.")
    return function_wrapper