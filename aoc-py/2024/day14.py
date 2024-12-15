from helpers import readdaylines
from dataclasses import dataclass
from collections import defaultdict
import re

lines = readdaylines(14, 2024, example=False)
# W, H = 11, 7  # exclusive size
W, H = 101, 103  # exclusive size

@dataclass
class Robot:
    pos: tuple[int, int]
    vec: tuple[int, int]

def parse():
    parsed = []
    for line in lines:
        px, py, vx, vy = map(int, re.findall(r"(-?\d+)", line))
        parsed.append(Robot((px, py), (vx, vy)))

    return parsed

def part1():
    seconds = 100
    robots = parse()

    moved = defaultdict(list)
    for robot in robots:
        pos_x, pos_y = robot.pos
        vec_x, vec_y = robot.vec
        moved[wrap_around(pos_x + (vec_x * seconds), W), wrap_around(pos_y + (vec_y * seconds), H)].append(robot)

    # lo inclusive, hi exclusize
    lo_x, hi_x = (0, W // 2), (W // 2 + 1, W)
    lo_y, hi_y = (0, H // 2), (H // 2 + 1, H)

    safe_factor = 1
    for quad1 in [lo_x, hi_x]:
        for quad2 in [lo_y, hi_y]:
            count = 0
            for x in range(*quad1):
                for y in range(*quad2):
                    count += len(moved[(x, y)])
            safe_factor *= count

    return safe_factor

def part2():
    """
    I won't do this. Maybe just check if no robots overlap.
    """
    seconds = 100
    robots = parse()

    for secs in range(seconds):
        print(f"DEBUGPRINT[6]: day14.py:52: secs={secs}")
        moved = defaultdict(list)
        for robot in robots:
            pos_x, pos_y = robot.pos
            vec_x, vec_y = robot.vec
            moved[wrap_around(pos_x + (vec_x * seconds), W), wrap_around(pos_y + (vec_y * seconds), H)].append(robot)
        d(moved)

def d(moved, end=""):
    for y in range(H):
        for x in range(W):
            print(f"{len(moved[(x, y)])}", end=end)
        print()

def wrap_around(num, size):
    return num % size
