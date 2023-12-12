from helpers import readdaylines
from operator import sub
from itertools import starmap

input = [[*map(int, line.split())] for line in readdaylines(9, 2023, example=False)]

# this one was too easy

def diff(line):
    lines = [line]
    while (not all(e == 0 for e in lines[-1])):
        lines.append([*starmap(sub, zip(lines[-1][1:], lines[-1]))])
    return lines

def solve(lines):
    if (len(lines) == 1):
        return 0
    else:
        return lines[0][-1] + solve(lines[1:])

def part1():
    return sum([solve(diff(line)) for line in input])

def solve2(lines):
    if (len(lines) == 1):
        return 0
    else:
        return lines[0][0] - solve2(lines[1:])

def part2():
    return sum([solve2(diff(line)) for line in input])