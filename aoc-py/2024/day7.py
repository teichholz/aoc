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
    ops = [add, mul]
    return solve(ops)

def part2():
    ops = [add, mul, lambda x, y: int(str(x) + str(y))]
    return solve(ops)

def solve(ops) -> int:
    sol = 0
    for equation in parse():
        eq, nums = equation

        res, *rest = nums
        result = [res]
        for num in rest:
            new_result = []
            for op in ops:
                for res in result:
                    new_result.append(op(res, num))
            result = new_result

        sol += eq * any(eq == num for num in result)

    return sol
