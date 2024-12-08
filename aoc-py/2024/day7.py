from helpers import readdaylines
from operator import add, mul

lines = readdaylines(7, 2024, example=False)

def parse() -> list[tuple[int, list[int]]]:
    out = list()
    for line in lines:
        eq, nums = line.split(": ")
        out.append((int(eq), list(map(int, nums.split()))))

    return out

def part1():
    return solve([add, mul])

def part2():
    return solve([add, mul, lambda x, y: int(str(x) + str(y))])

def solve(ops):
    total = 0
    for eq, nums in parse():
        results = [nums[0]]

        for num in nums[1:]:
            results = [
                op(res, num)
                for res in results
                for op in ops
                if res <= eq
            ]

        total += eq * any(eq == res for res in results)

    return total
