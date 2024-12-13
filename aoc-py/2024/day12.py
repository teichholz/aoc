from helpers import readdaylines, dirs4, dirs8, is_diag
from collections import defaultdict, Counter

lines = readdaylines(12, 2024, example=True)
W, H = len(lines[0]), len(lines)

def parse() -> list[list[str]]:
    return [list(line) for line in lines]

def part1():
    groups = group_cells(parse())

    s = 0
    for _, positions in groups.items():
        area = len(positions)
        perimeter = area * 4

        for pos_i in positions:
            for pos_j in positions:
                if pos_i == pos_j:
                    continue

                perimeter -= abs(pos_i[0] - pos_j[0]) == 1 and pos_i[1] == pos_j[1]
                perimeter -= abs(pos_i[1] - pos_j[1]) == 1 and pos_i[0] == pos_j[0]

        s += area * perimeter

    return s

def part2():
    groups = group_cells(parse())

    s = 0
    for letter, positions in groups.items():
        print(f"DEBUGPRINT[18]: day12.py:34: letter={letter}")
        area = len(positions)
        perimeter = list()
        for col, row in positions:
            for dcol, drow in dirs4:
                boundary = col + dcol, row + drow
                if boundary not in positions:
                    # boundaries will be added multiple times when we have concave corners (inner corners)
                    perimeter.append(boundary)

        print(f"DEBUGPRINT[20]: day12.py:37: perimeter={perimeter}")
        count = Counter(perimeter)
        print(f"DEBUGPRINT[22]: day12.py:46: count={count}")

        def find(start) -> int:
            cur = start
            last_dir = (0, 0)
            turns = 0

            while True:
                for dx, dy in dirs8:
                    if (dx, dy) == last_dir:
                        continue

                    neighbor = (col + dx, row + dy)
                    if neighbor in perimeter:
                        turns += is_diag((dx, dy)) * count[cur]
                        cur = neighbor

                if cur == start:
                    break

            return turns

        # unsolved
        sides = find(perimeter[0])
        print(f"DEBUGPRINT[19]: day12.py:66: sides={sides}")
        s += area * sides

    return s

def group_cells(grid) -> dict[str, set[tuple[int, int]]]:
    def dfs(col, row, letter) -> set[tuple[int, int]]:
        if not (0 <= row < H) or not (0 <= col < W):
            return set()

        if (col, row) in seen:
            return set()

        if grid[col][row] != letter:
            return set()

        seen.add((col, row))
        positions = set([(col, row)])

        for dx, dy in dirs4:
            positions |= dfs(col + dx, row + dy, letter)

        return positions

    seen = set()
    groups = defaultdict(set)
    ctr = 0

    for row in range(H):
        for col in range(W):
            letter = grid[row][col]
            group_positions = dfs(row, col, letter)
            if letter in groups and len(group_positions & groups[letter]) == 0 and len(group_positions) > 0:
                ctr += 1
                groups[letter + str(ctr)] |= group_positions
            else:
                groups[letter] |= group_positions

    return groups
