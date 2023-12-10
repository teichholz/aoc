from helpers import readdaylines
from itertools import groupby
from functools import reduce

input = [(hand, int(score)) for line in readdaylines(7, 2023) for hand, score in [line.split()]]

# Five of a kind, where all five cards have the same label: AAAAA
# Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# High card, where all cards' labels are distinct: 23456

def kind(hand: str) -> int:
    s = ''.join(sorted(hand))
    groups = groupby(s)
    match sorted([(k, len(list(a))) for k,a in groups], key=lambda x: x[1], reverse=True):
        case [(_, 5)]: return 7
        case [(_, 4), (_,1)]: return 6
        case [(_, 3), (_,2)]: return 5
        case [(_, 3), _, _]: return 4
        case [(_, 2), (_, 2), _]: return 3
        case [(_, 2), _, _, _]: return 2
        case [_, _, _, _, _]: return 1
    raise Exception("No match")

def addjoker(hand: str) -> str:
    s = ''.join(sorted(hand))
    groups = groupby(s)
    rest = sorted([(k, len(list(a))) for k,a in groups], key=lambda x: (x[1], strength[x[0]]), reverse=True)
    if (len(rest) == 0):
        return hand + 'A'
    else:
        return hand + rest[0][0]

cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
strength = {card: len(cards) - i for i, card in enumerate(cards)}
strength['J'] = 0 # part2
def chop(hand: str) -> int:
    return reduce(lambda acc, x: acc * len(cards) + x, [strength[c] for c in hand], 0)

def placejoker(hand: str) -> str:
    js = hand.count('J')
    hand = hand.replace('J', '')
    for _ in range(js):
        hand = addjoker(hand)
    return hand

ranked = [i*score for i,(hand, score) in enumerate(sorted(input, key=lambda hand: (kind(placejoker(hand[0])), chop(hand[0]))), 1)]
part = sum(ranked)