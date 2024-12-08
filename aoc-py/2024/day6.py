from helpers import readdaylines
from collections import defaultdict

lines = readdaylines(6, 2024, example=True)
W = len(lines[0])
H = len(lines)
input = {(row, col): char for row, line in enumerate(lines) for col, char in enumerate(line)}

def left(v):
    return v[1], -v[0]
def right(v):
    return -v[1], v[0]

def map(grid=lines):
    pos = "".join(grid).rfind("^")
    row, col = pos // W, pos % W

    cur = (row, col, -1, 0)

    seen = set()
    dirs = defaultdict(list)
    while True:
        row, col, drow, dcol = cur

        seen.add((row, col))
        dirs[(row, col)].append((drow, dcol))

        leaving = (row == 0 and drow == -1) or (row == H - 1 and drow == 1) or (col == 0 and dcol == -1) or (col == W - 1 and dcol == 1)
        if leaving:
            break

        if input[(row + drow, col + dcol)] == "#":
            dcol, drow = right((dcol, drow))

        cur = (row + drow, col + dcol, drow, dcol)

    return len(seen), seen, dirs

def p(seen, grid=lines):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (y, x) in seen:
                print("X", end="")
            else:
                print(cell, end="")
        print("")
