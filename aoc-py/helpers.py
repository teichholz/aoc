import functools
import os
from time import perf_counter_ns
from typing import Any, Callable, Final, Generator, Iterable, Literal, TextIO, TypeVar, overload
from typing import Optional

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


def cycle(iter: Iterable[T]) -> Generator[T, None, None]:
    while True:
        yield from iter


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


def manhatten(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(abs(x - y) for x, y in zip(a, b))


def add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(a, b))


def sub(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x - y for x, y in zip(a, b))


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

def visualize_points(points: list[tuple[int, int]],
                     markers: Optional[list[str]] = None,
                     empty_char: str = '.',
                     padding: int = 2,
                     show_axes: bool = True,
                     min_x: Optional[int] = None,
                     max_x: Optional[int] = None,
                     min_y: Optional[int] = None,
                     max_y: Optional[int] = None):
    """
    Visualize points on a grid.

    Args:
        points: List of (x, y) coordinates to display
        markers: Optional list of characters to use for each point.
                 If None, uses '1', '2', '3', ... for each point.
                 If a point appears multiple times, uses the first marker.
        empty_char: Character to use for empty cells
        padding: Number of cells to add around the bounding box
        show_axes: Whether to show axis labels
        min_x: Optional minimum x coordinate (overrides automatic calculation)
        max_x: Optional maximum x coordinate (overrides automatic calculation)
        min_y: Optional minimum y coordinate (overrides automatic calculation)
        max_y: Optional maximum y coordinate (overrides automatic calculation)
    """
    if not points and (min_x is None or max_x is None or min_y is None or max_y is None):
        print("No points to visualize")
        return

    # Find bounding box (or use provided values)
    if min_x is None:
        min_x = min(p[0] for p in points) if points else 0
    if max_x is None:
        max_x = max(p[0] for p in points) if points else 0
    if min_y is None:
        min_y = min(p[1] for p in points) if points else 0
    if max_y is None:
        max_y = max(p[1] for p in points) if points else 0

    # Add padding
    min_x = max(0, min_x - padding)
    max_x = max_x + padding
    min_y = max(0, min_y - padding)
    max_y = max_y + padding

    # Create grid
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    grid = [[empty_char for _ in range(width)] for _ in range(height)]

    # Determine markers
    if markers is None:
        markers = [str(i + 1) for i in range(len(points))]
    elif len(markers) < len(points):
        # Extend markers if not enough provided
        markers = markers + [str(i + 1) for i in range(len(markers), len(points))]

    # Mark points (if duplicate points, first marker wins)
    point_to_marker = {}
    for point, marker in zip(points, markers):
        if point not in point_to_marker:
            point_to_marker[point] = marker

    for point, marker in point_to_marker.items():
        x, y = point
        grid[y - min_y][x - min_x] = marker

    # Print grid (y-axis reversed for display)
    if show_axes:
        print("Grid visualization:")
        print(f"  X: {min_x} to {max_x}, Y: {min_y} to {max_y}")

    for y in range(height - 1, -1, -1):
        if show_axes:
            print(f"{y + min_y:3d} ", end="")
        for x in range(width):
            print(grid[y][x], end="")
        print()

    if show_axes:
        print("    ", end="")
        for x in range(width):
            print(str((x + min_x) % 10), end="")
        print()

    # Print point coordinates
    print("Points:", end=" ")
    for i, point in enumerate(points):
        marker = markers[i] if i < len(markers) else str(i + 1)
        print(f"{marker}={point}", end="  ")
    print()

