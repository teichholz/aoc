import helpers as h 
from functools import reduce
from collections import Counter
from operator import mul, or_

input = h.readdaylines(2, 2023)

def parse(line):
    p = line.split(': ')[1]
    ps = p.split('; ')
    return [dict(map(color, p.split(', '))) for p in ps]

def color(str):
    """
    '4 red' -> ('red', 4)
    """
    amount, color = str.split(' ')    
    return (color, int(amount))

sum, sum2 = 0, 0
bag = Counter({ 'red': 12, 'green': 13, 'blue': 14 })
for i, line in enumerate(input):
    g = parse(line)
    max = reduce(or_, [Counter(set) for set in g])

    if (bag >= max):
        sum += i + 1
    
    sum2 += reduce(mul, max.values())

print(f'part 1: {sum}\npart 2: {sum2}') 