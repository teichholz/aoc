from helpers import readdaylines

def parse(line):
    dir, n, color = line.split(' ')
    return dir, n, color
def parse2(line):
    _, _, color = line.split(' ')
    n = int(color[2:-2], base=16)
    dir = color[-2]
    return dir, n, color
input = [*map(parse2, readdaylines(18, 2023, example=False))]

dirmap = {'0': (1, 0), '1': (0, 1), '2': (-1, 0), '3': (0, -1), 'U': (0, -1),'D': (0, 1),'R': (1, 0),'L': (-1, 0)} 
def dir2vec(dir): return dirmap[dir]
def scalar(n, dir): return n * dir[0], n * dir[1]
def add(pos, dir): return pos[0] + dir[0], pos[1] + dir[1]

def part1(instrs=input):
    polygon = [(0,0)]
    R = 0
    for dir, n, _ in instrs:
        n = int(n)
        R += n
        polygon.append(add(polygon[-1], scalar(n, dir2vec(dir))))
  
    A = gauss(polygon)
    I = 1 + A - R / 2
    
    return R + I

def gauss(ps):
    """Gauss' area formula"""
    area = 0
    pss = [*ps, ps[0]]
    for i in range(len(ps)):
        area += pss[i][0] * pss[i+1][1] - pss[i][1] * pss[i+1][0]
    return area / 2
    