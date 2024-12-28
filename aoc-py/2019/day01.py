import os
from functools import cache

nums = list(map(int, os.fdopen(3, "r").readlines()))


def part1():
    return sum(num // 3 - 2 for num in nums)


def part2():
    return sum(map(fuel, nums))


@cache
def fuel(num):
    f = num // 3 - 2

    if f < 0:
        return 0

    return f + fuel(f)
