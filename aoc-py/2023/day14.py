from helpers import readdaylines, transpose

input = readdaylines(14, 2023, example=False)

def tilt(line, scandir=1):
    W = len(line)
    boundary = -1 if scandir == 1 else W
    inds = range(W) if scandir == 1 else range(W-1, -1, -1) 
    for i in inds:
        if line[i] == '#':
            boundary = i
        if line[i] == 'O':
            boundary = boundary+scandir
            line[boundary], line[i] = line[i], line[boundary]
    return line

def tiltall(grid):
    """
    nort -> west -> south -> east
    """
    southtilt = lambda l: tilt(l, scandir=-1)
    north = map(tilt, transpose(grid))
    west = map(tilt, transpose(north))
    south = map(southtilt, transpose(west))
    east = map(southtilt, transpose(south))
    return [*east]

def load(grid):
    """
    Takes the transposed grid as input
    """
    W = len(grid[0])
    sum = 0
    for line in grid:
        for i in range(W):
            if (line[i] == 'O'):
                sum += W - i
    return sum

def part1():
    tinput = transpose(input)
    return load(tilt(line) for line in tinput)

CYCLES = 1000000000
def part2():
    grid = input
    grids = {}
    for i in range(0, CYCLES):
        tupgrid = tuple(map(tuple, grid))
        if (tupgrid in grids):
            # check if cycle length divides the remaining cycles
            if ((CYCLES - i) % (i - grids[tupgrid]) == 0):
                return load(transpose(grid))
        grids[tupgrid] = i
        grid = tiltall(grid)
            