import os
import functools

def readday(day, year):
    home = os.environ["HOME"]
    with open(f"{home}/git/aoc/aoc-py/input/{year}/{day}", "r") as f:
        return f.read()

def openday(day, year): 
    home = os.environ["HOME"]
    return open(f"{home}/git/aoc/aoc-py/input/{year}/{day}", "r")

def readdaylines(day, year):
    return readday(day, year).splitlines()

def flatmap(f, xs):
    return [y for ys in xs for y in f(ys)]

def compose(*functions):
    return functools.reduce(lambda acc, g: lambda x: acc(g(x)), functions, lambda x: x)

def chunked(lst, n):
    if (isinstance(lst, map)):
        lst = list(lst)
    for i in range(0, len(lst), n):
        yield lst[i:i + n]