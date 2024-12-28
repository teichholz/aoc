import os
import sys
from itertools import product

input = list(map(int, os.fdopen(3, "r").read().strip().split(",")))


def part1():
    prog = list(input)
    prog[1] = 12
    prog[2] = 2
    ptr = 0
    while True:
        op = prog[ptr]
        if op == 1:
            out = prog[ptr + 3]
            lhs, rhs = prog[ptr + 1], prog[ptr + 2]
            prog[out] = prog[lhs] + prog[rhs]
        elif op == 2:
            out = prog[ptr + 3]
            lhs, rhs = prog[ptr + 1], prog[ptr + 2]
            prog[out] = prog[lhs] * prog[rhs]
        elif op == 99:
            break
        else:
            assert False

        ptr += 4

    return prog[0]


def part2():
    for noun, verb in product(range(100), range(100)):
        prog = list(input)
        ptr = 0
        prog[1] = noun
        prog[2] = verb
        while True:
            op = prog[ptr]
            if op == 1:
                out = prog[ptr + 3]
                lhs, rhs = prog[ptr + 1], prog[ptr + 2]
                prog[out] = prog[lhs] + prog[rhs]
            elif op == 2:
                out = prog[ptr + 3]
                lhs, rhs = prog[ptr + 1], prog[ptr + 2]
                prog[out] = prog[lhs] * prog[rhs]
            elif op == 99:
                break
            else:
                assert False

            ptr += 4

        if prog[0] == 19690720:
            return 100 * noun + verb

    return None


if not sys.flags.interactive:
    print(part1())
    print(part2())
