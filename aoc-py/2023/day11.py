from helpers import readdaylines, manhatten, transpose, flatmap
from itertools import combinations

input = [[c for c in line] for line in readdaylines(11, 2023, example=False)]

def part1(input=input):
    expanded = transpose(expand(transpose(expand(input))))
    W = len(expanded[0])
    H = len(expanded)
    points = []
    for y in range(H):
        for x in range(W):
            if (expanded[y][x] == '#'):
                points.append((x, y))
    dists = {}
    for p1, p2 in combinations(points, 2):
        dists[(p1, p2)] = manhatten(p1, p2)
    return sum(dists.values())

F = 1000000
def part2(input=input):
    expanded = input
    texpanded = transpose(expanded)
    W = len(expanded[0])
    H = len(expanded)

    points = []
    for y in range(H):
        for x in range(W):
            if (expanded[y][x] == '#'):
                points.append((x, y))

    space = {}
    for p1, p2 in combinations(points, 2):
        r1, r2 = (p1[1], p2[1]) if p1[1] < p2[1] else (p2[1], p1[1])
        yempty = sum(all(c == '.' for c in row) for row in expanded[r1+1:r2])
        c1, c2 = (p1[0], p2[0]) if p1[0] < p2[0] else (p2[0], p1[0])
        xempty = sum(all(c == '.' for c in row) for row in texpanded[c1+1:c2])
        space[(p1, p2)] = (yempty, xempty)
        
    dists = {}
    for p1, p2 in combinations(points, 2):
        sx, sy = space[(p1, p2)] 
        dists[(p1, p2)] = manhatten(p1, p2) + (sx + sy) * F - (sx + sy) 

    return sum(dists.values())

def expand(grid):
    return flatmap(lambda row: [row, row] if all(c == '.' for c in row) else [row], grid)
