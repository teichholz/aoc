from helpers import readdaylines

lines = readdaylines(6, 2024, example=False)
W = len(lines[0])
H = len(lines)
input = {(row, col): char for row, line in enumerate(lines) for col, char in enumerate(line)}

def right(v):
    return -v[1], v[0]

def part1():
    pos = "".join(lines).rfind("^")
    row, col = pos // W, pos % W
    start = (row, col, -1, 0)

    seen = sim(start)
    return len(seen)

def part2():
    pos = "".join(lines).rfind("^")
    row, col = pos // W, pos % W
    start = (row, col, -1, 0)

    seen = sim(start)

    os = set()
    for row, col in seen:
        save = input[(row, col)]
        input[(row, col)] = "#"

        try:
            sim(start)
        except Loop:
            os.add((row, col))

        input[(row, col)] = save

    return os

class Loop(Exception):
    pass

def sim(start, ctr=0):
    cur = start
    seen = set()
    while True:
        row, col, drow, dcol = cur

        seen.add((row, col))

        leaving = (row == 0 and drow == -1) or (row == H - 1 and drow == 1) or (col == 0 and dcol == -1) or (col == W - 1 and dcol == 1)
        if leaving:
            break

        if input[(row + drow, col + dcol)] == "#":
            dcol, drow = right((dcol, drow))
            cur = row, col, drow, dcol
        else:
            cur = (row + drow, col + dcol, drow, dcol)
            ctr += 1
            if (ctr > 2 * W * H):
                raise Loop

    return seen

def p(seen, grid=lines):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (y, x) in seen:
                print("X", end="")
            else:
                print(cell, end="")
        print("")
