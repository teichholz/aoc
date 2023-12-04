import helpers as h 
from functools import reduce
import operator
import re

input = h.readdaylines(2, 2023)

def parse(line):
    p = line.split(': ')[1]
    ps = p.split('; ')
    return [dict(map(game, p.split(', '))) for p in ps]


# '4 red' -> (red, 4)
def game(str):
    amount, color = str.split(' ')    
    return (color, int(amount))

bag = { 'red': 12, 'green': 13, 'blue': 14 }
def isValid(set):
    return not any([amount > bag[color] for color, amount in set.items()])

sum = 0
sum2 = 0
for i, line in enumerate(input):
    g = parse(line)

    if (all([isValid(set) for set in g])):
        sum += i + 1
    
    minBag = { 'red': 0, 'green': 0, 'blue': 0 }
    for set in g:
        for color, amount in set.items():
            minBag[color] = max(minBag[color], amount)
    sum2 += reduce(operator.mul, minBag.values())


print(sum) 
print(sum2) 