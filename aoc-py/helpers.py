import functools
import os
from time import perf_counter_ns
from typing import Any, Callable, Final, Generator, Iterable, Literal, TextIO, TypeVar, overload

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")

dirs: Final[list[tuple[int, int]]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
dirs4: Final[list[tuple[int, int]]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
dirs8: Final[list[tuple[int, int]]] = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def profiler(method: Callable[..., T]) -> Callable[..., T]:

    def wrapper_method(*args: Any, **kwargs: Any) -> T:
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


def is_diag(dir: tuple[int, int]) -> bool:
    return dir[0] * dir[1] != 0


def readday(day: str, year: int, example: bool = False) -> str:
    home = os.environ["HOME"]
    e = ".example" if example else ""
    with open(f"{home}/git/aoc/aoc-py/input/{year}/{day}{e}", "r") as f:
        return f.read()


def openday(day: str, year: int) -> TextIO:
    home = os.environ["HOME"]
    return open(f"{home}/git/aoc/aoc-py/input/{year}/{day}", "r")


def readdaylines(day: str, year: int, example: bool = False) -> list[str]:
    return readday(day, year, example).splitlines()


def transpose(xs: list[list[Any]]) -> list[list[Any]]:
    return [list(row) for row in zip(*xs)]


def flatmap(f: Callable[[U], list[V]], xs: list[U]) -> list[V]:
    return [y for ys in xs for y in f(ys)]


def cycle(l: Iterable[T]) -> Generator[T, None, None]:
    while True:
        yield from l


def reverse(f: Callable[..., T]) -> Callable[..., T]:
    return lambda *x: f(*reversed(x))


def compose(*functions: Callable[..., Any]) -> Callable[..., Any]:
    def identity(x: Any) -> Any:
        return x

    def compose_two(acc: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        def composed(*x: Any) -> Any:
            return acc(g(*x))
        return composed

    return functools.reduce(compose_two, functions, identity)


def chunked(lst: Iterable[T], n: int) -> Generator[list[T], None, None]:
    if isinstance(lst, map):
        lst = list(lst)
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def manhatten(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def sub(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def times(a: tuple[int, int], s: int) -> tuple[int, int]:
    return a[0] * s, a[1] * s


@overload
def sign(a: int | float) -> Literal[-1, 0, 1]: ...
@overload
def sign(a: int | float, b: int | float) -> Literal[-1, 0, 1]: ...
def sign(*args: int | float) -> Literal[-1, 0, 1]:
    if len(args) == 1:
        a = args[0]
        return 1 if a > 0 else -1 if a < 0 else 0
    if len(args) == 2:
        a, b, *_ = args
        return 1 if a > b else -1 if a < b else 0

    raise Exception("Can't handle args")