from helpers import readday
from functools import cache

input = readday(11, 2024, example=False)

def parse() -> list[int]:
    return list(map(int, input.strip().split()))

def solve():
    nums = parse()
    blinks = 75

    for _ in range(blinks):
        nums = [new for num in nums for new in apply_rule(num)]

    return len(nums)

def solve2():
    return rec(tuple(parse()), 75)

@cache
def rec(stones: tuple[int, ...], blinks_left: int) -> int:
    """
    This code is inspired by the recursive fibonacci algorithm.
    It does the same thing, but with different rules
    """
    if blinks_left == 0:
        return len(stones)

    return sum(rec(tuple(apply_rule(stone)), blinks_left - 1) for stone in stones)


def apply_rule(num: int) -> list[int]:
    if num == 0:
        return [1]

    s = str(num)
    digits = len(s)
    if digits % 2 == 0:
        mid = digits // 2
        lhs, rhs = int(s[:mid]), int(s[mid:])
        return [lhs, rhs]

    return [num * 2024]
