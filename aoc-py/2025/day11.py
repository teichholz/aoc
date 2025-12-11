import helpers as h
from functools import cache

input = h.readdaylines(11, 2025, example=False)

def parse(input: str):
    l, *r = input.replace(':', '').split(' ')
    return l, r

g = {l: r for l, r in [parse(line) for line in input]}

def part1():
    @cache
    def paths(cur = 'out', root = 'you'):
        if cur == root:
            return cur

        ps = []
        for parent, childs in g.items():
            if cur in childs:
                rps = paths(parent, root)
                if isinstance(rps, str):
                    ps.append(f"{cur} -> {rps}")
                else:
                    ps.extend([f"{cur} -> {p}" for p in rps])

        return ps

    return len(paths())

def part2():
    @cache
    def count_paths(cur, root, visited_dac, visited_fft):
        if cur == 'dac':
            visited_dac = True
        if cur == 'fft':
            visited_fft = True

        if cur == root:
            return 1 if visited_dac and visited_fft else 0

        total = 0
        for parent, childs in g.items():
            if cur in childs:
                total += count_paths(parent, root, visited_dac, visited_fft)

        return total

    return count_paths('out', 'svr', False, False)
