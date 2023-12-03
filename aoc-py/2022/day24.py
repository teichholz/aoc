import helpers as h
import copy as c

input = h.readdaylines(24, 2022)
tinput = [*map(lambda *x: x, *input)]
rows, cols = len(input), len(tinput)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __hash__(self):
        return hash(str(self))

def takecol(col):
    if (col == 0 or col == cols - 1):
        raise Exception(f"No reason to take first or last column: {col}")
    if (col == 1 or col == cols - 2):
        return ['.'] * rows
    return tinput[col][1:-1]

def takerow(row):
    if (row == 0 or row == rows - 1):
        return ['.'] * cols

    return input[row][1:-1]

def blizzardinrange(line, cur, t, r = '>', l = '<'):
    ln = len(line)
    return line[(cur - t) % ln] == r or line[(cur + t) % ln] == l

def neighbours(p):
    if (p == start): return [Point(start.x, start.y + 1), p]
    if (p == Point(120, 25)): return [goal]
    ns = [Point(p.x + 1, p.y),
          Point(p.x, p.y + 1),
          p,
          Point(p.x - 1, p.y),
          Point(p.x, p.y - 1)]
    ps = [p for p in ns if input[p.y][p.x] != '#']
    return ps

start = Point(1, 0)
goal = Point(120, 26)
def bfs():
    open = {start}
    t = 0
    while True:
        all = set()
        t += 1
        for o in open:
            for n in neighbours(o):
                vert = blizzardinrange(takerow(n.y), n.x-1, t)
                hor = blizzardinrange(takecol(n.x), n.y-1, t, 'v', '^')
                if (vert or hor):
                    continue
                all.add(n)
        if (goal in all):
            return t
        open = all