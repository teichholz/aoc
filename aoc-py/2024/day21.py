from typing import Callable, List
from functools import cache
from helpers import readdaylines

codes = readdaylines(21, 2024, example=False)

def part1():
    complexity = 0
    for code in codes:
        print(f"DEBUGPRINT[58]: day21.py:9: code={code}")
        path_len = length(code, 3)
        print(f"DEBUGPRINT[59]: day21.py:11: path_len={path_len}")
        num = int(code[:-1])
        print(f"DEBUGPRINT[60]: day21.py:13: num={num}")
        complexity += path_len * num

    return complexity

@cache
def length(code: str, depth: int) -> int:
    if depth == 0:
        return len(code)

    moves = zip("A" + code, code)
    possible_paths = [paths(*move) for move in moves]

    # all possible combinations
    codes = list(possible_paths[0])
    for ps in possible_paths[1:]:
        new_codes = []
        for code in codes:
            for p in ps:
                new_codes.append(code + p)
        codes = new_codes

    return min(length(code, depth - 1) for code in codes)


@cache
def paths(start_let: str, end_let: str) -> list[str]:
    pad = NUMPAD if start_let in NUMPAD and end_let in NUMPAD else DIRPAD
    start = pad[start_let]
    end = pad[end_let]

    illegal = 3 if pad == NUMPAD else 0

    diff = end - start
    drow, dcol = int(diff.real), int(diff.imag)
    ver = ("^" * -drow) + ("v" * drow)
    hor = ("<" * -dcol) + (">" * dcol)

    pref_ver = illegal.real == start.real  # same row

    if pref_ver:
        return [ver + hor + "A"]
    else:
        return [hor + ver + "A", ver + hor + "A"]


def coords_num(let: str):
    rows_num = ["789", "456", "123", "0A"]
    cols_num = ["741", "8520", "963A"]
    return coord(rows_num, cols_num)(let)

def coords_dir(let: str):
    rows_dir = ["^A", "<v>"]
    cols_dir = ["<", "^v", "A>"]
    return coord(rows_dir, cols_dir)(let)


def coord(rows: List[str], cols: List[str]) -> Callable[[str], complex]:
    def inner(let: str):
        row, col = -1, -1
        for i, str in enumerate(rows):
            if let in str:
                row = i

        for i, str in enumerate(cols):
            if let in str:
                col = i

        if row == -1 or col == - 1:
            raise Exception(f"Unknown coordinate {let}")

        return row + col * 1j
    return inner


NUMPAD = {let: coords_num(let) for let in "0123456789A"}
DIRPAD = {let: coords_dir(let) for let in "<>^vA"}

def part2():
    pass
