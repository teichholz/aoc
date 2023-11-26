import helpers as h
import numpy
import re

input = h.readdaylines(19, 2022)

# this solution is from https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j1jr1cg/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# i'm merely trying to get some python skills
V = lambda *a: numpy.array(a)
key = lambda a: tuple(a[0]+a[1]) + tuple(a[1])
prune = lambda x: sorted({key(x):x for x in x}.values(), key=key)[-1000:]

def parse(line):
    i,a,b,c,d,e,f = map(int, re.findall(r'\d+',line))
    return (i, (V(0,0,0,a), V(0,0,0,1)),    # Cost and production
               (V(0,0,0,b), V(0,0,1,0)),    # of each robot type,
               (V(0,0,d,c), V(0,1,0,0)),    # in the order geode,
               (V(0,f,0,e), V(1,0,0,0)),    # obs, clay, and ore.
               (V(0,0,0,0), V(0,0,0,0)))    # Construct no robot.

def run(blueprint, t):
    todo = [(V(0,0,0,0), V(0,0,0,1))]       # What we have and make.
    for t_ in range(t,0,-1):
        todo_ = list()                      # Queue for the next minute.
        for have, make in todo:
            for cost, more in blueprint:
                if all(cost <= have):       # We can afford this robot.
                    todo_.append((have+make-cost, make+more))
        todo = prune(todo_)                 # Prune the search queue.
    return max(have[0] for have, _ in todo)

part1, part2 = 0, 1
for i, *blueprint in map(parse, input):
    part1 += run(blueprint, 24) * i
    part2 *= run(blueprint, 32) if i<4 else 1

print(part1, part2)