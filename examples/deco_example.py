import useful_decorators
import time

@useful_decorators.timeit
@useful_decorators.local_saving("temp", "pickle")
def computation_func(a, b):
    time.sleep(a)
    return range(b)

print(computation_func(0.5, 1000))