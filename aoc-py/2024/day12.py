from helpers import readdaylines, dirs4
from collections import defaultdict

lines = readdaylines(12, 2024, example=False)
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
    for _, positions in groups.items():
        area = len(positions)
        perimeter = set()
        for col, row in positions:
            pos = col, row
            for dcol, drow in dirs4:
                boundary = col + dcol, row + drow
                if boundary not in positions:
                    perimeter.add((pos, boundary))

        def extract(perimeter, hor=True) -> set[tuple[tuple[int, int], tuple[int, int]]]:
            """
            Extracts horizontal or vertical edges
            """
            edges = set()
            for fr, to in perimeter:
                if hor and abs(fr[0] - to[0]) == 1:
                    edges.add((fr, to))
                if not hor and abs(fr[1] - to[1]) == 1:
                    edges.add((fr, to))

            return edges

        def connect_edges(cur, dirs, perimeter, seen=set()) -> set[tuple[tuple[int, int], tuple[int, int]]]:
            """
            Tries to connect loose edges, building one continuous edge
            """
            fr, to = cur

            if cur in seen:
                return set()

            seen.add(cur)
            positions = set([cur])

            for drow, dcol in dirs:
                from_row, from_col = fr
                to_row, to_col = to
                neighbor = ((from_row + drow, from_col + dcol), (to_row + drow, to_col + dcol))
                if neighbor in perimeter:
                    positions |= connect_edges(neighbor, dirs, perimeter, seen)

            return positions

        # extract all the horizontal edges in the perimeter and try connect them, if they are continuous
        hor_edges = extract(perimeter, True)
        continuous_hor_edges = list()
        while len(hor_edges) > 0:
            continuous = connect_edges(hor_edges.pop(), [(0, 1), (0, -1)], hor_edges, set())
            hor_edges -= continuous
            continuous_hor_edges.append(continuous)

        # any rectilinear polygon has the same amount of vertical and horizontal edges
        s += area * len(continuous_hor_edges) * 2

    return s

def group_cells(grid) -> dict[str, set[tuple[int, int]]]:
    def dfs(row, col, letter) -> set[tuple[int, int]]:
        if not (0 <= row < H) or not (0 <= col < W):
            return set()

        if (row, col) in seen:
            return set()

        if grid[row][col] != letter:
            return set()

        seen.add((row, col))
        positions = set([(row, col)])

        for dcol, drow in dirs4:
            positions |= dfs(row + drow, col + dcol, letter)

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
