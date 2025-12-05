import helpers as h

input = h.readday(5, 2025, example=False)


def parse(input: str) -> tuple[list[tuple[int, int]], list[int]]:
    [ranges, ids] = input.split('\n\n')
    iranges = [tuple(map(int, range.split('-'))) for range in ranges.splitlines()]
    iids = [int(id) for id in ids.splitlines()]
    return (iranges, iids)

def in_range(range: tuple[int, int], id: int) -> bool:
    """Check if an id is in a range. Inclusive."""
    return id >= range[0] and id <= range[1]

def part1():
    ranges, ids = parse(input)
    sum = 0

    for id in ids:
        fresh = False
        for range in ranges:
            if in_range(range, id):
                fresh = True
                break

        if fresh:
            sum += 1

    return sum

def part2():
    ranges, _ = parse(input)

    merged = merge_ranges(ranges)
    fresh = 0
    for range in merged:
        fresh += range[1] - range[0] + 1

    return fresh

def merge_ranges(ranges):
    # Sort by start point
    ranges.sort(key=lambda x: x[0])

    merged = [ranges[0]]

    for current in ranges[1:]:
        last = merged[-1]

        # If current overlaps with last merged range
        if current[0] <= last[1]:
            # Merge by extending the end point
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            # No overlap, add as new range
            merged.append(current)

    return merged