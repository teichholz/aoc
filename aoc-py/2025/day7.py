import helpers as h
from functools import cache

input = h.readdaylines(7, 2025, example=False)

def parse(input: list[str]):
    return input

def part1():
    parsed = parse(input)
    start_row, start_col = 0, len(parsed[0]) // 2
    assert parsed[start_row][start_col] == 'S', "Wrong start"

    @cache
    def trace_beam(row: int, col: int):
        if row < 0 or col < 0 or row >= len(parsed) or col >= len(parsed[row]):
            return set()

        if parsed[row][col] == '^':
            result = {(row, col)}
            result.update(trace_beam(row + 1, col - 1))
            result.update(trace_beam(row + 1, col + 1))
            return result

        if parsed[row][col] == '.' or parsed[row][col] == 'S':
            return trace_beam(row + 1, col)

        return set()

    hit_splitters = trace_beam(start_row, start_col)
    return len(hit_splitters)

def part2():
    """
    Can also be seen as how many different paths there are, a beam can take to reach the end
    """
    parsed = parse(input)
    start_row, start_col = 0, len(parsed[0]) // 2
    assert parsed[start_row][start_col] == 'S', "Wrong start"

    @cache
    def trace_beam(row: int, col: int):
        if row < 0 or col < 0 or row >= len(parsed) or col >= len(parsed[row]):
            return 0

        # Each splitter creates a new timeline
        if parsed[row][col] == '^':
            return 1 + trace_beam(row + 1, col - 1) + trace_beam(row + 1, col + 1)

        if parsed[row][col] == '.' or parsed[row][col] == 'S':
            return trace_beam(row + 1, col)

        return 0

    # initial timeline + timelines created by splitters
    return 1 + trace_beam(start_row, start_col)