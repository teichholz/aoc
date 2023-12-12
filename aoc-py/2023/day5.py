from helpers import readday, flatmap, chunked
from functools import partial

input = readday(5, 2023).split("\n\n")

seeds = [int(line) for line in input[0].split('seeds: ')[1].split()]
seedranges = [range(s, s + o) for s, o in chunked(seeds, 2)]
mapss = [s.splitlines() for s in input[1:]]

def parserange(line):
    dest, src, rng = [int(i) for i in line.split()]
    ro = range(src, src + rng)
    rd = range(dest, dest + rng)
    return (ro, rd)

def parseblock(block: list):
    return [parserange(line) for line in block]

def parsemap(lines):
    return parseblock(lines[1:])

def part2():
    s = [*seedranges]
    for m in map(parsemap, mapss):
        s = flatmap(partial(mapseedrange, m), s)
    return min(seed.start for seed in s)

def mapseedrange(map, seedr):
    for ro, rd in map:
        if (intersection(seedr, ro)):
            return maprange(seedr, ro, rd)
    return [seedr]

def maprange(rin: range, ro: range, rd: range) -> list:
    l = list()
    if (rin.start < ro.start):
        l.append(range(rin.start, min(rin.stop, ro.start)))
    if (ri := intersection(rin, ro)):
        l.append(range(ri.start - ro.start + rd.start, ri.stop - ro.start + rd.start))
    if (rin.stop > ro.stop):
        l.append(range(max(rin.start, ro.stop), rin.stop))
    return l
    
def intersection(r1, r2):
    if r1.stop > r2.start and r2.stop > r1.start:  
        return range(max(r1.start, r2.start), min(r1.stop, r2.stop))
    else:
        return None  