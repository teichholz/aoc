from helpers import readdaylines
import heapq

lines = readdaylines(17, 2023, example=True)
W = len(lines[0])
H = len(lines)
input = {(row, col): int(char) for row, line in enumerate(lines) for col, char in enumerate(line)}

def left(v):
    return v[1], -v[0]
def right(v):
    return -v[1], v[0]

def dik(grid=input):
    q = [(0, (0, 0), (0, 1), 0), (0, (0, 0), (1, 0), 0)]
    seen = set()

    while q:
        d, cur, cdir, n = heapq.heappop(q)

        if cur == (W - 1, H - 1) and n >= 3:
            return d, n

        if (cur, cdir, n) in seen:
            continue
        seen.add((cur, cdir, n))

        for dir in [cdir] if n < 3 else [cdir, left(cdir), right(cdir)]:
            nxt = (cur[0] + dir[0], cur[1] + dir[1])

            if nxt not in grid:
                continue
            nextn = 0 if cdir != dir else n + 1
            if nextn >= 10:
                continue

            heapq.heappush(q, (d + grid[nxt], nxt, dir, nextn))
