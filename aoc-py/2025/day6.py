import helpers as h
from functools import reduce
from itertools import groupby
from operator import add, mul

input = h.readday(6, 2025, example=False)

def parse(input: str):
    lines = input.splitlines()
    nums = [list(map(int, line.split())) for line in lines[:-1]]
    ops = lines[-1].split()
    return nums, ops

def part1():
    nums, ops = parse(input)
    transposed = list(map(list, zip(*nums)))
    sum = 0
    for i, op in enumerate(ops):
        if op == '+':
            nums = transposed[i]
            reduced = reduce(add, nums)
            sum += reduced
        elif op == '*':
            nums = transposed[i]
            reduced = reduce(mul, nums)
            sum += reduced

    return sum

def part2():
    lines = input.splitlines()
    nums = [''.join(line).strip() for line in zip(*lines[:-1])]
    cols = [[int(x) for x in group] for key, group in groupby(nums, key=lambda x: x != '') if key]

    ops = lines[-1].split()

    sum = 0
    for i, op in enumerate(ops):
        if op == '+':
            nums = cols[i]
            reduced = reduce(add, nums)
            sum += reduced
        elif op == '*':
            nums = cols[i]
            reduced = reduce(mul, nums)
            sum += reduced

    return sum