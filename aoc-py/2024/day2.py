import helpers as h

# num pairs between 10000 and 99999
input = h.readdaylines(2, 2024, example=False)


def parse(line: str) -> list[int]:
    return [int(num) for num in line.split()]


def part1():
    """
    This solution is not appropriate for day 2, since the first number is not "removable" (skippable inside the loop)
    """
    ls = [parse(line) for line in input]
    count = 0
    for nums in ls:
        inc, dec, diff = True, True, True
        prev, *tail = nums
        for num in tail:
            inc &= num > prev
            dec &= num < prev
            diff &= 1 <= abs(num - prev) <= 3

            prev = num

        safe = (inc ^ dec) and diff
        count += safe

    return count

def part2():
    ls = [parse(line) for line in input]

    def is_safe(row):
        inc = [row[i + 1] - row[i] for i in range(len(row) - 1)]
        return set(inc) <= {1, 2, 3} or set(inc) <= {-1, -2, -3}

    return sum([any([is_safe(row[:i] + row[i + 1:]) for i in range(len(row))]) for row in ls])
