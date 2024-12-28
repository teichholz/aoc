from collections import deque

from helpers import readday

input = readday(15, 2024, example=True)


def parse() -> tuple[list[str], str]:
    grid, moves = input.strip().split("\n\n")

    grid = grid.split()
    moves = "".join(moves.split())

    return grid, moves


grid, moves = parse()
W, H = len(grid[0]), len(grid)
start = [
    (row, col)
    for row, line in enumerate(grid)
    for col, char in enumerate(line)
    if char == "@"
][0]
grid = {
    (row, col): char for row, line in enumerate(grid) for col, char in enumerate(line)
}

# easier problem without dots
temp = dict(grid)
for pos, char in temp.items():
    if char == ".":
        del grid[pos]


def part1():
    pos = start
    for move in moves:
        d = dir(move)
        try:
            news = try_move(pos, d)
            del grid[pos]
            pos = add(pos, d)
            for row, col, char in news:
                grid[(row, col)] = char
        except Wall:
            pass

    sum = 0
    for pos, char in grid.items():
        if char == "O":
            row, col = pos
            sum += 100 * row + col

    return sum


def part2():
    # enlarge width
    global grid
    global W
    W = 2 * W
    wgrid = {}
    for (row, col), char in grid.items():
        lmap = {"O": "[", ".": ".", "@": "@", "#": "#"}
        rmap = {"O": "]", ".": ".", "@": ".", "#": "#"}
        wgrid[row, col * 2] = lmap[char]
        wgrid[row, col * 2 + 1] = rmap[char]

    pos = (start[0], start[1] * 2)
    for move in moves[:100]:
        print(f"DEBUGPRINT[90]: day15.py:71: move={move}")
        gc = dict(wgrid)
        first = set()
        move_dir = dir(move)
        try:
            q = deque([pos])
            while q:
                p = q.popleft()
                col_row = None
                if move in "<>":
                    col_row = p[0]
                else:
                    col_row = p[1]

                assert p in wgrid
                newp = add(move_dir, p)
                if newp in wgrid and wgrid[newp] == "#":
                    raise Wall()
                gc[newp] = wgrid[p]
                if col_row not in first:
                    del gc[p]

                first.add(col_row)

                if newp in wgrid:
                    q.append(newp)
                    if move in "^v":
                        if wgrid[newp] == "[":
                            other = (newp[0], newp[1] + 1)
                            q.append(other)
                        if wgrid[newp] == "]":
                            other = (newp[0], newp[1] - 1)
                            q.append(other)

            pos = add(pos, move_dir)
            wgrid = gc
            d(grid=gc, W=W)

        except Wall:
            print("ran into wall")
            # noop, this direction can't be moved in
            pass

    d(grid=wgrid, W=W)

    sum = 0
    for pos, char in wgrid.items():
        if char == "[":
            row, col = pos
            sum += 100 * row + col

    return sum


def d(grid=grid, W=W, H=H):
    for row in range(H):
        for col in range(W):
            if (row, col) in grid:
                print(f"{grid[(row, col)]}", end="")
            else:
                print(".", end="")
        print()


dirs = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}


def dir(move: str) -> tuple[int, int]:
    if move not in dirs:
        raise Exception("Unknown move")

    return dirs[move]


new_entries = set[tuple[int, int, str]]


def try_move(pos: tuple[int, int], dir: tuple[int, int]) -> new_entries:
    if grid[pos] == "#":
        raise Wall(f"At {pos}")

    if pos not in grid:
        return []

    new = add(pos, dir)
    return [(new[0], new[1], grid[pos])] + try_move(new, dir)


class Wall(Exception):
    pass


def add(a, b) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b) -> tuple[int, int]:
    return (a[0] - b[0], a[1] - b[1])
