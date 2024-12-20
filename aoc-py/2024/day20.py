from helpers import readdaylines
from collections import deque

lines = readdaylines(20, 2024, example=False)
grid = {(row, col): char for row, line in enumerate(lines) for col, char in enumerate(line) if char == "#"}
W, H = len(lines[0]), len(lines)

def part1():
    sum = 0
    for wall in grid:
        for diff in [(1, 0), (0, 1)]:
            start = add(wall, diff)
            end = sub(wall, diff)
            if in_range(*start) and in_range(*end) and start not in grid and end not in grid:
                path = bfs(grid, start, end)
                pico = len(path) - 1 - 2  # start doest not count + subtract cheat cost
                if pico >= 100:
                    sum += 1

    return sum

def part2():
    pass

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

            if in_range(*neighbor) and neighbor not in grid and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    raise Exception("No path")

def add(v1, v2):
    return tuple(a + b for a, b in zip(v1, v2))

def sub(v1, v2):
    return tuple(a - b for a, b in zip(v1, v2))

def in_range(row, col):
    return 0 <= row < H and 0 <= col < W

def d():
    for row in range(H):
        for col in range(W):
            if (row, col) in grid:
                print("#", end="")
            else:
                print(".", end="")
        print()
