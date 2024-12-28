import functools
import os
from time import perf_counter_ns
from typing import Any

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
dirs8 = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def profiler(method):

    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter_ns()
        ret = method(*args, **kwargs)
        stop_time = perf_counter_ns() - start_time
        time_len = min(9, ((len(str(stop_time)) - 1) // 3) * 3)
        time_conversion = {
            9: "seconds",
            6: "milliseconds",
            3: "microseconds",
            0: "nanoseconds",
        }
        print(
            f"Method {method.__name__} took : {
                stop_time / (10**time_len)} {time_conversion[time_len]}"
        )
        return ret

    return wrapper_method


def is_diag(dir):
    return dir[0] * dir[1] != 0


def readday(day, year, example=False):
    home = os.environ["HOME"]
    e = ".example" if example else ""
    with open(f"{home}/git/aoc/aoc-py/input/{year}/{day}{e}", "r") as f:
        return f.read()


def openday(day, year):
    home = os.environ["HOME"]
    return open(f"{home}/git/aoc/aoc-py/input/{year}/{day}", "r")


def readdaylines(day, year, example=False):
    return readday(day, year, example).splitlines()


def transpose(xs):
    return [list(row) for row in zip(*xs)]


def flatmap(f, xs):
    return [y for ys in xs for y in f(ys)]


def cycle(l):
    while True:
        yield from l


def reverse(f):
    return lambda *x: f(*reversed(x))


def compose(*functions):
    return functools.reduce(
        lambda acc, g: lambda *x: acc(g(*x)), functions, lambda x: x
    )


def chunked(lst, n):
    if isinstance(lst, map):
        lst = list(lst)
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def manhatten(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] + b[0], a[1] + b[1]


def times(a, s):
    return a[0] * s, a[1] * s


def sign(*args):
    if len(args) == 1:
        a = args[0]
        return 1 if a > 0 else -1 if a < 0 else 0
    if len(args) == 2:
        a, b, *_ = args
        return 1 if a > b else -1 if a < b else 0

    raise Exception("Can't handle args")
