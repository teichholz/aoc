import helpers as h
import math
from itertools import combinations

input = h.readdaylines(8, 2025, example=False)

def dist(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> float:
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

def parse(input: list[str]):
    return [tuple(map(int, line.split(','))) for line in input]

def part1():
    parsed= parse(input)
    comps = { coord: set([coord]) for coord in parsed }

    prod = list(combinations(parsed, 2))
    prod = sorted(prod, key=lambda x: dist(x[0], x[1]))

    connections = prod[:1000]
    for p1, p2 in connections:
        if comps[p1] is comps[p2]:
            continue

        old_set = comps[p2]
        comps[p1].update(old_set)
        for box in old_set:
            comps[box] = comps[p1]

    unique_comps = list({id(c): c for c in comps.values()}.values())
    biggest = sorted(unique_comps, key=len, reverse=True)

    return len(biggest[0]) * len(biggest[1]) * len(biggest[2])


def part2():
    parsed= parse(input)
    comps = { coord: set([coord]) for coord in parsed }

    prod = list(combinations(parsed, 2))
    prod = sorted(prod, key=lambda x: dist(x[0], x[1]))

    connections = prod
    last = None
    for p1, p2 in connections:
        if comps[p1] is comps[p2]:
            continue

        old_set = comps[p2]
        comps[p1].update(old_set)
        for box in old_set:
            comps[box] = comps[p1]

        if all(comp is comps[p1] for comp in comps.values()):
            last = p1, p2
            break

    p1, p2 = last
    p1_x = p1[0]
    p2_x = p2[0]

    return p1_x * p2_x