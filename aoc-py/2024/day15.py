from helpers import readday

input = readday(15, 2024, example=True)
def parse() -> tuple[list[str], str]:
    grid, moves = input.strip().split("\n\n")

    grid = grid.split()
    moves = "".join(moves.split())

    return grid, moves


grid, moves = parse()
W, H = len(grid[0]), len(grid)
start = [(row, col) for row, line in enumerate(grid) for col, char in enumerate(line) if char == "@"][0]
grid = {(row, col): char for row, line in enumerate(grid) for col, char in enumerate(line)}

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
    new_grid = {}
    for (row, col), char in grid.items():
        lmap = {"O": "[", ".": ".", "@": "@", "#": "#"}
        rmap = {"O": "]", ".": ".", "@": ".", "#": "#"}
        new_grid[row, col * 2] = lmap[char]
        new_grid[row, col * 2 + 1] = rmap[char]
    grid = new_grid

    pos = add(start, (0, start[1]))
    for move in moves:
        move_dir = dir(move)
        try:
            news, olds = try_move2(pos, move_dir)
            for old in olds:
                del grid[old]
            for row, col, char in news:
                grid[(row, col)] = char
            pos = add(pos, move_dir)
        except Wall:
            # noop, this direction can't be moved in
            pass

    sum = 0
    for pos, char in grid.items():
        if char == "[":
            row, col = pos
            sum += 100 * row + col

    return sum

def d():
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


new_entries = list[tuple[int, int, str]]
old_entries = list[tuple[int, int]]
def try_move(pos: tuple[int, int], dir: tuple[int, int]) -> new_entries:
    if grid[pos] == "#":
        raise Wall(f"At {pos}")

    if pos not in grid:
        return []

    new = add(pos, dir)
    return [(new[0], new[1], grid[pos])] + try_move(new, dir)

def try_move2(pos: tuple[int, int], dir: tuple[int, int]) -> tuple[new_entries, old_entries]:
    if not 0 <= pos[0] <= H or not 0 <= pos[1] < W:
        raise Exception("Invariance: Boundary is walled off")

    if pos not in grid:
        return [], []

    if grid[pos] == "#":
        raise Wall(f"At {pos}")

    # if dir is up or down and we move a box
    if dir in [(1, 0), (-1, 0)] and grid[pos] in ["[", "]"]:
        # we want to also move the other part of the box
        new_pos = add(pos, dir)
        col_diff = {"[": 1, "]": -1}
        pos2 = (pos[0], pos[1] + col_diff[grid[pos]])
        new_pos2 = add(pos2, dir)
        news, olds = try_move2(new_pos, dir)
        news2, olds2 = try_move2(new_pos2, dir)
        return [(new_pos[0], new_pos[1], grid[pos]), (new_pos2[0], new_pos2[1], grid[pos2])] + news + news2, [pos, pos2] + olds + olds2
    else:
        new_pos = add(pos, dir)
        news, olds = try_move2(new_pos, dir)
        return [(new_pos[0], new_pos[1], grid[pos])] + news, [pos] + olds

class Wall(Exception):
    pass

def add(a, b) -> tuple[int, int]:
    return tuple(map(sum, zip(a, b)))
