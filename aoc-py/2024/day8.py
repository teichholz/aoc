from helpers import readdaylines
from collections import defaultdict

lines = readdaylines(8, 2024, example=False)
M = {(row, col): char for row, line in enumerate(lines) for col, char in enumerate(line)}
A = defaultdict(list)
for coord, char in M.items():
    if char != ".":
        A[char].append(coord)
W, H = len(lines[0]), len(lines)

def part1():
    antis = set()
    for _, coords in A.items():
        for a in coords:
            for b in coords:
                if a == b:
                    continue

                b_to_a = sub(a, b)
                anti = add(b, scale(b_to_a, 2))
                if in_grid(anti):
                    antis.add(anti)

    return antis

def part2():
    antis = set()
    for _, coords in A.items():
        for a in coords:
            for b in coords:
                if a == b:
                    continue

                b_to_a = sub(a, b)
                anti = add(b, b_to_a)
                while in_grid(anti):
                    antis.add(anti)
                    anti = add(anti, b_to_a)

    return antis

def p(anodes):
    for row in range(W):
        for col in range(H):
            if (row, col) in anodes:
                print("#", end="")
            else:
                print(M[(row, col)], end="")
        print()

def add(v1, v2):
    return tuple(a + b for a, b in zip(v1, v2))

def sub(v1, v2):
    return tuple(a - b for a, b in zip(v1, v2))

def scale(v, scalar):
    return tuple(scalar * x for x in v)

def in_grid(v):
    col, row = v
    return 0 <= col < W and 0 <= row < H
