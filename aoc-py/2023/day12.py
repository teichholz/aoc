from functools import cache
from helpers import readdaylines

def parse(line):
    springs, groups = line.split()
    return (springs, eval(groups))
input = [parse(line) for line in readdaylines(12, 2023, example=False)]

@cache
def solve(conditions, groups):
    if not groups:
        return 0 if "#" in conditions else 1 
    if not conditions:
        return 1 if not groups else 0
    
    c, *cs = conditions
    g, *gs = groups
    
    if c == '#':
        if g == 1 and (not cs or cs[0] in '.?'):
            return solve(('.', *cs[1:]), tuple(gs))
        if cs and cs[0] in '#?':
            return solve(('#', *cs[1:]), (g-1, *gs))
        return 0
    if c == '.':
        return solve(tuple(cs), groups)
    if c == '?':
        return solve(('#', *cs), groups) + solve(('.', *cs), groups)
    
def part1():
    return sum(solve('?'.join([s]*5), g*5) for s, g in input)