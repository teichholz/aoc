from helpers import readdaylines
from collections import deque

lines = readdaylines(18, 2024, example=False)
lines2 = list(map(lambda row: tuple(map(int, row.split(","))), lines))[1024:]
lines = list(map(lambda row: tuple(map(int, row.split(","))), lines))[:1024]
grid = {(row, col) for col, row in lines}
W, H = 71, 71

def part1():
    return len(bfs(grid, (0, 0), (H - 1, W - 1))) - 1

def part2():
    for col, row in lines2:
        grid.add((row, col))
        try:
            bfs(grid, (0, 0), (H - 1, W - 1))
        except Exception:
            return f"{col},{row}"

def bfs(grid, start, goal):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    queue = deque([(start, [start])])

    visited = set()
    visited.add(start)

    while queue:
        (current_row, current_col), path = queue.popleft()

        if (current_row, current_col) == goal:
            return path

        for dr, dc in directions:
            neighbor = (current_row + dr, current_col + dc)

            if in_range(neighbor) and neighbor not in grid and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    raise Exception("No path")

def in_range(coord):
    return 0 <= coord[0] < H and 0 <= coord[1] < H

def d():
    for row in range(H):
        for col in range(W):
            if (row, col) in grid:
                print("#", end="")
            else:
                print(".", end="")
        print()
