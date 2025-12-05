import helpers as h

input = h.readdaylines(3, 2025, example=False)


def parse(line: str) -> list[int]:
    return list(map(int, line))


def part1():
    parsed = [parse(line) for line in input]

    return find_max_joltage(2, parsed)

def part2():
    parsed = [parse(line) for line in input]

    return find_max_joltage(12, parsed)

def find_max_joltage(banks: int, lines: list[list[int]]) -> int:
    sum = 0
    for line in lines:
        max_i = 0
        max_joltage = 0

        for bank in range(banks, 0, -1):
            max = 0
            for i, joltage in enumerate(line):
                if joltage > max and i < len(line) - bank + 1:
                    max = joltage
                    max_i = i
            line = line[max_i + 1:]
            max_joltage = max_joltage * 10 + max

        sum += max_joltage

    return sum