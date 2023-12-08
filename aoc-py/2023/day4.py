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
    if (not goodNumbers):
        return 0
    return 2 ** (len(goodNumbers) - 1)

lines = list(map(parse, input))
part1 = int(sum(map(score, lines)))

def part2():
    bonus = Counter({})
    for i, game in enumerate(lines, 1):
        bonus += Counter({k:(bonus[i] + 1) for k in after(i, len(game[0] & game[1])) if k <= len(lines)})

    return len(lines) + sum(bonus.values())
   
def after(i, count):
    return list(range(i + 1, i + 1 + count))