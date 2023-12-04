import helpers as h 
from functools import reduce
import operator
import re

input = h.readdaylines(2, 2023)

def parse(line):
    p = line.split(': ')[1]
    ps = p.split('; ')
    pss = [list(map(game, p.split(', '))) for p in ps]
    
    l = list()
    for s in pss:
        d = dict()
        for turn in s:
            color, amount = turn
            d[color] = amount
        l.append(d)
    return l


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
    gameIsValid = True
    for set in g:
        if(not isValid(set)):
            gameIsValid = False
            break

    if (gameIsValid):
        sum += i + 1
    
    minBag = { 'red': 0, 'green': 0, 'blue': 0 }
    for set in g:
        for color, amount in set.items():
            minBag[color] = max(minBag[color], amount)
    sum2 += reduce(operator.mul, minBag.values())

    # [1, 2, 3]
    # f = lambda acc, x: 
    # identität i = f(i, x) = x
    # f(l[n], ..., f(l[2], f(l[1], f(l[0], i)))


print(sum) 
print(sum2) 