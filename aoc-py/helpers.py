import os
import functools

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

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
    return functools.reduce(lambda acc, g: lambda *x: acc(g(*x)), functions, lambda x: x)

def chunked(lst, n):
    if (isinstance(lst, map)):
        lst = list(lst)
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
def manhatten(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def sign(a, b):
    return 1 if a > b else -1 if a < b else 0