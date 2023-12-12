from helpers import readdaylines, cycle
from functools import reduce
from math import lcm

input = readdaylines(8, 2023, example=False)
turns = [*map(lambda x: 0 if x == 'L' else 1 ,list(input[0]))]
nodes = input[2:]

d = reduce(lambda acc, x: {**acc, **x}, [{k: eval(v)} for node in nodes for k, v in [node.split(' = ')]], {})

def part1():
    cur = 'AAA'
    ts = cycle(turns)
    depth = 0
    while cur != 'ZZZ':
        depth += 1
        cur = d[cur][next(ts)]
    return depth

def part2():
    cycles = []
    for node in {k for k in {*d} if k.endswith('A')}:
        cur = node 
        for depth, turn in enumerate(cycle(turns), 1):
            cur = d[cur][turn]
            if (cur.endswith('Z')):
                cycles.append(depth)
                break
    print(len(turns))
    print(cycles)

    return lcm(*cycles)