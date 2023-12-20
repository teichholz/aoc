# The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:
# - If the beam encounters empty space (.), it continues in the same direction.
# - If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
# - If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
# - If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.
from helpers import readdaylines

input = readdaylines(16, 2023, example=False)

# Use complex nummbers if you want to code golf this problem

def left(v):
    return v[1], -v[0]

def right(v):
    return -v[1], v[0]

def inbounds(pos):
    return 0 <= pos[0] < len(input[0]) and 0 <= pos[1] < len(input)

def add(pos, dir):
    return pos[0] + dir[0], pos[1] + dir[1]

def solve(start=(0, 0), dir=(1, 0)):
    q = [(start, dir)]
    marked = set()
    while len(q) > 0:
        pos, dir = q.pop()
        if (inbounds(pos) and (pos, dir) not in marked):
            marked.add((pos, dir))
            ch = input[pos[1]][pos[0]]
            if ch == '/':
                if (dir[0] != 0):
                    q.append((add(pos, left(dir)), left(dir)))
                else:
                    q.append((add(pos, right(dir)), right(dir)))
            elif ch == '\\':
                if (dir[0] != 0):
                    q.append((add(pos, right(dir)), right(dir)))
                else:
                    q.append((add(pos, left(dir)), left(dir)))
            elif ch == '|' and dir[0] != 0:
                q.append((add(pos, left(dir)), left(dir)))
                q.append((add(pos, right(dir)), right(dir)))
            elif ch == '-' and dir[1] != 0:
                q.append((add(pos, left(dir)), left(dir)))
                q.append((add(pos, right(dir)), right(dir)))
            else:
                q.append((add(pos, dir), dir))

    return len({pos for pos, _ in marked})

def part1():
    return solve()

def part2():
    H = len(input)
    W = len(input[0])
    right = (1, 0)
    left = (-1, 0)
    up = (0, -1)
    down = (0, 1)
    rights = map(lambda y: ((0, y), right), range(H))
    lefts = map(lambda y: ((W-1, y), left), range(H))
    downs = map(lambda x: ((x, 0), down), range(W))
    ups = map(lambda x: ((x, H-1), up), range(W))
    return max(solve(pos, dir) for pos, dir in list(rights) + list(lefts) + list(downs) + list(ups))