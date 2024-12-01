import helpers as h

# num pairs between 10000 and 99999
input = h.readdaylines(1, 2024)


def parse(line: str) -> (int, int):
    l, r = line.split()
    return (int(l), int(r))


def part1():
    ls = [parse(line) for line in input]

    lids, rids = h.transpose(ls)
    slids, srids = sorted(lids), sorted(rids)
    ds = [abs(lid - rid) for (lid, rid) in zip(slids, srids)]

    return sum(ds)

def part2():
    from collections import Counter
    ls = [parse(line) for line in input]

    lids, rids = h.transpose(ls)
    rc = Counter(rids)

    ds = [lid * rc[lid] for lid in lids]

    return sum(ds)
