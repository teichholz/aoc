from helpers import readdaylines, dirs

# in, out
top, right, bottom, left = -1j, 1, 1j, -1
pipes = {
    '|': [top, bottom],
    '-': [left, right],
    'F': [right, bottom],
    '7': [left, bottom],
    'J': [top, left],
    'L': [top, right],
}

input = [[c for c in line] for line in readdaylines(10, 2023, example=False)]
W = len(input[0])
H = len(input)
S = (74, 18) # row, col

def part1():
    ps = [[pipes.get(c, [0, 0]) for c in line] for line in input] 
    ps[S[0]][S[1]] = pipes.get(start(ps))
    dists = { S: 0 }
    cur = S
    f = 0
    while (True):
        prev_dist = dists[cur]
        row, col = cur
        f, *_ = [i for i in ps[row][col] if i != -f]
        cur = (row + int(f.imag), col + int(f.real))
        dists[cur] = prev_dist + 1
        if (cur == S):
            break

    for y in range(H):
        for x in range(W):
            if ((y, x) not in dists):
                input[y][x] = '.'
    
    return (max(dists.values()) + 1) / 2

def part2():
    """
    good ol point in polygon test
    """
    count = 0
    for y in range(H):
        for x in range(W):
            if (input[y][x] != "."):
                continue 
            
            dy = 1
            dx = 1
            crosses = 0
            while (y + dy < H and x + dx < W):
                c = input[y + dy][x + dx]
                if (c in {*pipes} - {'L', '7'}):
                    crosses += 1
                dy += 1
                dx += 1
                
            if crosses % 2 == 1:
                count += 1
    return count

def start(ps) -> str:
    """
    could be a lot nicer
    """
    row, col = S
    for pipe, v in pipes.items():
        conn = 0
        for dx, dy in dirs:
            a = ps[row + dy][col + dx]
            if (dx == 1):
                if (left in a and right in v):
                    conn += 1
            elif (dx == -1):
                if (right in a and left in v):
                    conn += 1
            elif (dy == 1):
                if (top in a and bottom in v):
                    conn += 1
            else:
                if (bottom in a and top in v):
                    conn += 1
        if (conn == 2):
            return pipe
            
    raise Exception('no start pipe found')
            