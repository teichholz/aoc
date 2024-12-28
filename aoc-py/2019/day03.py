import os

input = os.fdopen(3, "r").read().strip()


def parse():
    lines = input.split("\n")
    return [line.split(",") for line in lines]


def part1():
    wire1, wire2, *_ = wires

    wire1_path, _ = get_path(wire1)
    wire2_path, _ = get_path(wire2)

    intersections = wire1_path & wire2_path

    return min(abs(x) + abs(y) for x, y in intersections)


def part2():
    wire1, wire2, *_ = wires

    wire1_path, wire1_list = get_path(wire1)

    wire2_path, wire2_list = get_path(wire2)

    intersections = wire1_path & wire2_path

    return min(wire1_list.index(p) + wire2_list.index(p) + 2 for p in intersections)


wires = parse()


def get_path(wire):
    col, row = 0, 0
    path = set()
    lpath = list()

    for instruction in wire:
        direction = instruction[0]
        length = int(instruction[1:])

        for _ in range(length):
            if direction == "R":
                col += 1
            elif direction == "L":
                col -= 1
            elif direction == "U":
                row += 1
            elif direction == "D":
                row -= 1
            path.add((col, row))
            lpath.append((col, row))

    return path, lpath
