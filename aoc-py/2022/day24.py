import helpers as h
import heapq as q
import copy as c

input = h.readdaylines(24, 2022)
tinput = [*map(lambda *x: x, *input)]
# try out python classes for once
class Point:
    def __init__(self, x, y, g=0, h=0, parent=None):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
        self.waited = 0
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __str__(self):
        return f"({self.x}, {self.y}) : g={self.g}, h={self.h}, f={self.f}"

def takecol(col):
    if (col == 0 or col == len(tinput) - 1):
        raise Exception(f"No reason to take first or last column: {col}")
    if (col == 1 or col == len(tinput) - 2):
        return ['.'] * (len(input) - 2)
    return tinput[col][1:-1]

def takerow(row):
    if (row == 0 or row == len(input) - 1):
        return ['.'] * (len(tinput) - 2)

    return input[row][1:-1]

def blizzardinrange(line, cur, t, r = '>', l = '<'):
    """
    line without walls
    """
    ln = len(line)
    t = t % ln # keep t in the range of the line
    d = t # direct distance

    return line[(cur - d) % ln] == r or line[(cur + d) % ln] == l
    
# a*
def h(p1, p2): return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def neighbours(p):
    if (p == start): return [Point(start.x, start.y + 1)] # From the start we can only go down
    ns = [Point(p.x + 1, p.y),
          Point(p.x - 1, p.y),
          Point(p.x, p.y + 1),
          Point(p.x, p.y - 1)]
    return [p for p in ns if input[p.y][p.x] != '#']

start = Point(1, 0)
goal = Point(120, 26)
def astar():
    s = Point(1, 0, 0, h(start, goal))
    open = [s]
    closed = []
    while (len(open) > 0):
        cur = q.heappop(open)
        if (cur == goal):
            return cur
        
        ns = neighbours(cur)
        for n in ns + [c.copy(cur)]:
            if (n != cur):
                ng = cur.g + 1
            else:
                n.waited += 1
                
            nh = h(n, goal)
            n.parent = cur
            n.g = ng
            n.h = nh
            n.f = ng + nh

            # filter neighbours based on the blizzards
            # note that n.g is equal to the time it took to get to n
            print(n)
            vert = blizzardinrange(takerow(n.y), n.x, n.g + n.waited)
            hor = blizzardinrange(takecol(n.x), n.y, n.g + n.waited, 'v', '^')
            if (vert or hor):
                continue
            
            if any(o.f < n.f for o in open + closed if o == n):
                continue

            q.heappush(open, n)
        q.heappush(closed, cur)
    




