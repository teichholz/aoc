from functools import cache
from helpers import readdaylines

codes = readdaylines(21, 2024, example=False)

def part1():
    return sum(int(code[:-1]) * length(code, 3) for code in codes)

def part2():
    return sum(int(code[:-1]) * length(code, 26) for code in codes)


NUMPAD = {'7': 0, '8': 1, '9': 2, '4': 1j, '5': 1 + 1j, '6': 2 + 1j,
          '1': 2j, '2': 1 + 2j, '3': 2 + 2j, ' ': 3j, '0': 1 + 3j, 'A': 2 + 3j}
DIRPAD = {' ': 0, '^': 1, 'A': 2, '<': 1j, 'v': 1 + 1j, '>': 2 + 1j}

@cache
def path(start, end):
    pad = NUMPAD if (start in NUMPAD and end in NUMPAD) else DIRPAD
    diff = pad[end] - pad[start]
    dcol, drow = int(diff.real), int(diff.imag)
    ver = ("^" * -drow) + ("v" * drow)
    hor = ("<" * -dcol) + (">" * dcol)

    ill = pad[" "] - pad[start]

    # ill == drow * 1j end is in the row of ill
    # ill != drow * 1j end is not in the row of ill
    # dcol > 0         path goes to the right
    # ill == dcol      end is in the column of ill
    prefer_ver_first = (dcol > 0 or ill == dcol) and ill != drow * 1j
    return (ver + hor if prefer_ver_first else hor + ver) + "A"

@cache
def length(code, depth):
    if depth == 0:
        return len(code)

    return sum(length(path(code[i - 1], c), depth - 1)
               for i, c in enumerate(code))
