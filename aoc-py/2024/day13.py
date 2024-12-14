from helpers import readday
from dataclasses import dataclass, astuple
import re
from sympy import symbols, Eq, solve

input = readday(13, 2024, example=False)

@dataclass
class Arcade:
    a_x: int
    a_y: int
    b_x: int
    b_y: int
    price_x: int
    price_y: int

def parse():
    segs = input.strip().split("\n\n")
    parsed = []
    for seg in segs:
        a, b, price = seg.split("\n")
        a_x, a_y = re.findall(r"(\d+)", a)
        b_x, b_y = re.findall(r"(\d+)", b)
        price_x, price_y = re.findall(r"(\d+)", price)
        parsed.append(Arcade(*map(int, [a_x, a_y, b_x, b_y, price_x, price_y])))

    return parsed

def part1():
    """
    Optimization problem
    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400

    objective fun (a costs 3, b costs 1):
    3 * a + b

    equality contraint:
    a * 94 + b * 22 = 8400
    a * 34 + b * 67 = 5400

    1 <= a <= 100
    1 <= b <= 100
    """
    arcades = parse()

    solutions = list()
    for arcade in arcades:
        solution = None
        min = float("inf")
        for a in range(1, 101):
            for b in range(1, 101):
                if constraint(arcade, a, b):
                    obj = objective(a, b)
                    if obj < min:
                        min = obj
                        solution = (a, b)
        solutions.append(solution)

    return solutions, sum(objective(*sol) if sol else 0 for sol in solutions)

def part2():
    """
    Optimization problem
    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400

    objective fun (a costs 3, b costs 1), I don't know why I don't need to consider this:
    3 * a + b

    equality contraint:
    a * 94 + b * 22 = 8400 + 10000000000000
    a * 34 + b * 67 = 5400 + 10000000000000
    """
    arcades = parse()

    inc = 10000000000000
    solutions = list()
    a, b = symbols('a b', integer=True)
    for arcade in arcades:
        a_x, a_y, b_x, b_y, price_x, price_y = astuple(arcade)

        eq1 = Eq(a * a_x + b * b_x, price_x + inc)
        eq2 = Eq(a * a_y + b * b_y, price_y + inc)

        solution = solve((eq1, eq2), (a, b))
        solutions.append(solution)

    return solutions, sum(objective(sol[a], sol[b]) if sol else 0 for sol in solutions)

def objective(a, b):
    return 3 * a + b

def constraint(arcade: Arcade, a: int, b: int):
    a_x, a_y, b_x, b_y, price_x, price_y = astuple(arcade)
    return a * a_x + b * b_x == price_x and a * a_y + b * b_y == price_y
