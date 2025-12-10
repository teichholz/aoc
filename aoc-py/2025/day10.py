import helpers as h
from collections import deque
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

input = h.readdaylines(10, 2025, example=True)

def parse(input: list[str]):
    """
    [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    indicator: [.##.] -> (False, True, True, False, False) The target state for the indicators
    wirings: [(1,3), (2), (2,3), (0,2), (0,1)] -> [(1,3), (2), (2,3), (0,2), (0,1)] What indicators are toggled
    joltage: {3,5,4,7} ->[3,5,4,7] The joltage of the wirings
    """
    blocks = input.split(' ')
    indicator = parse_indicator(blocks[0])
    wirings = [parse_parens(wiring) for wiring in blocks[1:-1]]
    joltage = parse_joltage(blocks[-1])
    return indicator, wirings, joltage

def parse_indicator(str: str) -> tuple[..., bool]:
    str = str.removeprefix('[')
    str = str.removesuffix(']')
    return tuple(map(lambda x: x == '#', str))

def parse_parens(str: str) -> tuple[..., int]:
    str = str.removeprefix('(')
    str = str.removesuffix(')')
    return tuple(map(int, str.split(',')))

def parse_joltage(str: str) -> tuple[..., int]:
    str = str.removeprefix('{')
    str = str.removesuffix('}')
    return tuple(map(int, str.split(',')))

def part1():
    parsed = [parse(block) for block in input]
    sum = 0
    for indicator, wirings, _ in parsed:
        result = bfs(indicator, wirings)
        if result is not None:
            sum += result
        else:
            print(f"Target {indicator} is unreachable")

    return sum

def bfs(target: tuple[..., bool], wirings: list[tuple[..., int]]):
    current = tuple(False for _ in range(len(target)))
    queue = deque([(current, 0)])
    visited = {current}

    while queue:
        state, presses = queue.popleft()

        if state == target:
            return presses

        for wiring in wirings:
            new_state = list(state)
            for pos in wiring:
                new_state[pos] = not new_state[pos]
            new_state = tuple(new_state)

            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, presses + 1))

    return None

def part2():
    parsed = [parse(block) for block in input]
    sum = 0
    for _, wirings, joltages in parsed:
        min_presses = find_min_joltage_combination(wirings, joltages)
        if min_presses is not None:
            sum += min_presses
        else:
            print(f"Target joltages {joltages} unreachable with wirings {wirings}")

    return sum

def find_min_joltage_combination(wirings: list[tuple[int, ...]], joltages: tuple[int, ...]) -> int | None:
    """
    Function was AI generated.
    Find minimum button presses to reach target joltage levels.

    Each button (wiring) affects multiple counters. For example:
    - Button (1,3) increases counters 1 and 3 by 1 each press
    - We need to reach joltages {3,5,4,7} for counters 0,1,2,3

    This creates a system of equations (one per counter):
    - For each counter i: sum of (presses of buttons that affect counter i) = joltages[i]

    Minimize: total button presses
    """
    num_buttons = len(wirings)
    num_counters = len(joltages)

    # Objective: minimize total button presses (sum of all press counts)
    c = np.ones(num_buttons)

    # Build constraint matrix: A[counter_i][button_j] = 1 if button j affects counter i
    A_eq = np.zeros((num_counters, num_buttons))
    for button_idx, wiring in enumerate(wirings):
        for counter_idx in wiring:
            A_eq[counter_idx][button_idx] = 1

    b_eq = np.array(joltages)

    constraints = LinearConstraint(A_eq, lb=b_eq, ub=b_eq)

    # All variables must be non-negative integers
    integrality = np.ones(num_buttons)
    bounds = Bounds(lb=np.zeros(num_buttons), ub=np.inf)

    # Solve the ILP
    result = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)

    if result.success:
        return int(round(result.fun))
    else:
        return None

def encode(wirings: list[tuple[..., int]], joltage: tuple[..., int]) -> tuple[tuple[..., int], int]:
    """
    Encodes the wirings and joltages as (ints, int).
    Essentially moves this problem into a managable problem space solvable by easy math.

    Example:
    (0), (1, 2), (2, 0) {5, 10, 5} -> (1, 1010, 1001) 5105
    (1), (3), (2, 3) {1, 10, 4, 7} -> (10, 10000, 10100) 11047
    """
    def concat(joltage: tuple[..., int]) -> str:
        return ''.join(map(str, joltage))

    new_joltage = int(concat(joltage))
    new_wirings = []
    for wiring in wirings:
        num = 0
        for pos in wiring:
            num += int('1' + ('0' * len(concat(joltage[len(joltage)-pos:]))))
        new_wirings.append(num)


    return tuple(new_wirings), new_joltage