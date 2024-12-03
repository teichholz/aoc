import helpers as h
import re
from dataclasses import dataclass

# num pairs between 10000 and 99999
input = h.readday(3, 2024, example=False)

class Instr:
    pass

@dataclass
class Mul(Instr):
    lhs: int
    rhs: int

class Do(Instr):
    pass

class Dont(Instr):
    pass

def parse(prog: str) -> list[Instr]:
    instrs = re.findall(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", prog)
    prog = []
    for instr in instrs:
        match instr:
            case expr if (match := re.match(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)", instr)):
                lhs, rhs = map(int, match.groups())
                prog.append(Mul(int(lhs), int(rhs)))
            case "do()":
                prog.append(Do())
            case "don't()":
                prog.append(Dont())
    return prog

def part1():
    prog = parse(input)
    total = 0

    for instr in prog:
        match instr:
            case Mul(lhs, rhs):
                total += lhs * rhs

    return total

def part2():
    prog = parse(input)
    total = 0

    do = True
    for instr in prog:
        match instr:
            case Mul(lhs, rhs) if do:
                total += lhs * rhs
            case Do():
                do = True
            case Dont():
                do = False

    return total
