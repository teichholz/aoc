from itertools import starmap
from operator import add

from helpers import profiler, readday, transpose

input = readday(25, 2024, example=False).strip()


def parse():
    schematics = input.split("\n\n")
    locks = [
        schematic.split()
        for schematic in schematics
        if all(c == "#" for c in schematic[0])
    ]
    keys = [
        schematic.split()
        for schematic in schematics
        if all(c == "#" for c in schematic[-1])
    ]

    return locks, keys


locks, keys = parse()


@profiler
def part1():
    hlocks = list(map(heights, locks))
    hkeys = list(map(heights, keys))

    sum = 0
    for hlock in hlocks:
        for hkey in hkeys:
            fitted = list(starmap(add, zip(hlock, hkey)))

            if all(fit <= 5 for fit in fitted):
                sum += 1

    return sum


def heights(schematic: list[str]) -> list[int]:
    return [col.count("#") - 1 for col in transpose(schematic)]


@profiler
def part2():
    pass
