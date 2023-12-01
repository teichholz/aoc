import helpers as h
import re

input = h.readdaylines(22, 2022)
board = [line.ljust(150, ' ') for line in input[0:-2]]
tboard = [list(row) for row in zip(*board)]
path = input[-1]

steps = [e if e.isalpha() else int(e) for e in re.findall(r'(\d+|\D)', path)]

def r(dir):
    return (-dir[1], dir[0])
def l(dir):
    return (dir[1], -dir[0])

def walk(path):
    pos = nextlineindex(board, (0, 0), 1)
    print(pos)
    dir = (1, 0)
    for c in path:
        if isinstance(c, int):
            for _ in range(c):
                pos = next(pos, dir)
                print(dir, pos)
        else:
            if c == 'R':
                dir = r(dir)
            else:
                dir = l(dir)
    return score(pos, dir)

def next(pos: (int, int), dir: (int, int)):
    """
    Returns the next position given the current position and direction
    """
    # branch on direction
    if dir == (1, 0) or dir == (-1, 0):  # horizontal
        return nextlineindex(board, pos, dir[0])
    elif dir == (0, 1) or dir == (0, -1):  # vertical
        (x, y) = nextlineindex(tboard, (pos[1], pos[0]), dir[1])
        return (y, x)


def nextlineindex(board, pos: (int, int), dir: -1 | 1):
    line = board[pos[1]]
    curx = pos[0]
    mod = len(line)
    # search for next '.' reset when '#' is found
    while True: 
        i = (curx + dir) % mod
        next = line[i]
        if (next == '.'):
            curx = i
            break
        elif (next == '#'):
            curx = pos[0]
            break
        elif (next == ' '):
            curx = i 
    

    return (curx, pos[1])

def score(pos, dir):
    return 4 * (pos[0] + 1) + 1000 * (pos[1] + 1) + facingscore(dir)

def facingscore(dir):
    if dir == (1, 0):
        return 0
    elif dir == (0, 1):
        return 1
    elif dir == (-1, 0):
        return 2
    elif dir == (0, -1):
        return 3