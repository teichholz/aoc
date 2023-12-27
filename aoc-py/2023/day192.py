from helpers import readday
from functools import reduce
import re

LT, GT = '<', '>'
def parseflow(flow): 
    name, rules = re.findall(r'(\w+)\{(.*)\}', flow)[0]
    rs = []
    for r in rules.split(','):
        if (r.isalpha()):
            thn = r
            rs.append(thn)
        else:
            cond, thn = r.split(':')
            lhs, rhs = cond[0], int(cond[2:])
            op = LT if cond[1] == '<' else GT
            rs.append((lhs, op, rhs, thn)) 

    return name, rs

flows = [ls.splitlines() for ls in readday(19, 2023, example=False).split('\n\n')][0]
flows = {k:v for k, v in map(parseflow, flows)}

bs = { 'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000) }
setmax = lambda bs, k, v: {**bs, k: (bs[k][0], v)}
setmin = lambda bs, k, v: {**bs, k: (v, bs[k][1])}

def solve(cur='in', bs=bs):
    combs = 1
    os = 0
    
    if cur == 'A':
        for min, max in bs.values():
            combs *= (max - min) + 1
        return combs + os
        
    if cur == 'R':
        return 0

    for rule in flows[cur]:
        if isinstance(rule, str):
            return os + solve(rule, bs)

        lhs, op, rhs, thn = rule
        if op == LT:
            os += solve(thn, setmax(bs, lhs, rhs-1))
            bs = setmin(bs, lhs, rhs)
        else:
            os += solve(thn, setmin(bs, lhs, rhs+1))
            bs = setmax(bs, lhs, rhs)
    
    raise Exception('No rule found')
part2 = solve    