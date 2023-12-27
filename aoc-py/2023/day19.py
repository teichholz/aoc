from helpers import readday
from functools import reduce
import re

def parseflow(flow): 
    name, rules = re.findall(r'(\w+)\{(.*)\}', flow)[0]
    rs = []
    for r in rules.split(','):
        if (re.fullmatch(r'[a-zA-Z]+', r)):
            thn = r
            rs.append(lambda : thn)
        else:
            cond, thn = r.split(':')
            # was lambda : thn if eval(cond) else None before
            # this was one of the nastiest bugs I've ever had to fix
            rs.append(lambda cond=cond, thn=thn: thn if eval(cond) else None) 
    return name, reduce(lambda acc, f: lambda : f() or acc(), [*reversed(rs)], lambda : None)

parsepart = eval # I changed the input to be valid map literals
flows, parts = [ls.splitlines() for ls in readday(19, 2023, example=False).split('\n\n')]
flows, parts = {k:v for k, v in map(parseflow, flows)}, [*map(parsepart, parts)]

def part1():
    sum = 0
    for part in parts:
        gs = globals()
        for key, value in part.items():
            gs[key] = value

        cur = 'in'
        while True: 
            cur = flows[cur]()

            if cur == 'A':
                sum += x + a + m + s
                break
            if cur == 'R':
                break
    return sum        