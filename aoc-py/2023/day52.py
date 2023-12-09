from helpers import compose, chunked
import helpers as h

input = h.readday(5, 2023).split("\n\n")
seeds = [int(line) for line in input[0].split('seeds: ')[1].split()]
mapss = [s.splitlines() for s in input[1:]]

def parseRange(line):
    dest, src, rng = [int(i) for i in line.split()]
    srcRang = range(src, src + rng)
    mapping = lambda seed: seed - src + dest
    return (srcRang, mapping)

def parseBlock(block: list):
    return [parseRange(line) for line in block]

def parseMap(lines):
    return parseBlock(lines[1:])

maps = list(map(parseMap, mapss))

def maptof(map):
    def f(seed):
        for range, mapping in map:
            if seed in range:
                return mapping(seed)
        return seed
    return f

mothermap = compose(*map(maptof, reversed(maps)))

part1 = min(map(mothermap, seeds))