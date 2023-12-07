import helpers as h 
from collections import Counter

input = h.readdaylines(4, 2023)

def parse(line: str):
    _, rhs = line.split(': ')
    our, winning = rhs.split(' | ')
    our = [int(num) for num in our.split()]
    winning = [int(winning) for winning in winning.split()]
    return (set(our), set(winning))

def score(game):
    our, winning = game
    goodNumbers = our & winning
    if (len(goodNumbers) == 0):
        return 0
    return 2 ** (len(goodNumbers) - 1)

lines = list(map(parse, input))
part1 = int(sum(map(score, lines)))

def part2():
    bonus = Counter({})
    for i, game in enumerate(lines, 1):
        sco = len(game[0] & game[1])

        inc = Counter({index:1 for index in after(i, sco) if index <= len(lines)})
        if (sco > 0): # if we win
            bonus += Counter({k:v*(bonus[i] + 1) for k, v in inc.items()})

    return len(lines) + sum(bonus.values())
   
def after(i, count):
    return list(range(i + 1, i + 1 + count))