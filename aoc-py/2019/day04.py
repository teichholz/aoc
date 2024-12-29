import os
import sys

input = os.fdopen(3, "r").read().strip()


lo, hi = 158126, 624574


def part1():
    cs = [two_same, inc]

    total = 0
    for p in range(lo, hi + 1):
        all = True
        for c in cs:
            if not c(str(p)):
                all = False
                break

        if all:
            total += 1

    return total


def two_same(p: str):
    for i, c in enumerate(p[1:]):
        if c == p[i]:
            return True

    return False


def inc(p: str):
    for i, c in enumerate(p[1:]):
        if c < p[i]:
            return False

    return True


def part2():
    cs = [two_same2, inc]

    total = 0
    for p in range(lo, hi + 1):
        all = True
        for c in cs:
            if not c(str(p)):
                all = False
                break

        if all:
            total += 1

    return total


def two_same2(p: str):
    seen = set()
    for i, c in enumerate(p[:-1]):
        found = c == p[i + 1]
        if c not in seen and found:
            longer_than_two = i + 2 < len(p) and c == p[i + 2]
            if not longer_than_two:
                return True
        seen.add(c)

    return False


if not sys.flags.interactive:
    print(part1())
    print(part2())
