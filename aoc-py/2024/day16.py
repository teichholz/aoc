from helpers import readdaylines
import heapq

lines = readdaylines(16, 2024, example=True)
W, H = len(lines[0]), len(lines)
grid = {(row, col): char for row, line in enumerate(lines) for col, char in enumerate(line)}
start = (H - 2, 1)
end = (1, W - 2)

def part1():
    return dijkstra(start, (0, 1), 0, end)[0][0]

def part2():
    sols = dijkstra(start, (0, 1), 0, end)
    return sols

def dijkstra(start, start_dir, start_cost, end):
    queue = []
    heapq.heappush(queue, (start_cost, start, start_dir, set()))
    seen_cost = dict()

    solutions = []

    while queue:
        cost, cur, dir, path = heapq.heappop(queue)

        if (cur, dir) in seen_cost and seen_cost[(cur, dir)] < cost:
            continue

        if grid[cur] == "#":
            continue

        if cur == end:
            solutions += [(cost, path)]

        seen_cost[(cur, dir)] = cost

        news = [(cost + 1, add(cur, dir), dir), (cost + 1000, cur, left(*dir)), (cost + 1000, cur, right(*dir))]
        for new in news:
            new_cost, new_pos, new_dir = new
            if (new_pos, new_dir) not in seen_cost or new_cost < seen_cost[(new_pos, new_dir)]:
                seen_cost[(new_pos, new_dir)] = new_cost
                heapq.heappush(queue, (new_cost, new_pos, new_dir, path | {cur}))

    return solutions

def add(pos, dir):
    return (pos[0] + dir[0], pos[1] + dir[1])

def right(row, col):
    return (col, -row)

def left(row, col):
    return (-col, row)
