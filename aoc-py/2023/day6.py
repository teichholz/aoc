from helpers import readdaylines
from operator import mul
from functools import reduce
from itertools import starmap

input = readdaylines(6, 2023)
times = [int(line) for line in [''.join(input[0].split(':')[1].split())]]
dists = [int(line) for line in [''.join(input[1].split(':')[1].split())]]
speeds = [*zip(times, dists)]

def scorebeatertimes(t, score):
    return [t for v, t in zip(range(0, t + 1), range(t, -1, -1)) if t * v > score]

part1 = reduce(mul, map(len, starmap(scorebeatertimes, speeds)))