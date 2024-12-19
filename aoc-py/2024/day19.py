from helpers import readday
from functools import cache

input = readday(19, 2024, example=False).strip()


# towel stripes range (my input) [1,9]
# pattern len ranges (my input) [40, 60]
def parse():
    towels, patterns = input.split("\n\n")
    towels = set(towels.split(", "))
    patterns = patterns.split()
    return towels, patterns


towels, patterns = parse()
lo = min(map(len, towels))
hi = max(map(len, towels))

def part1():
    sum = 0
    for pattern in patterns:
        found = search(pattern, towels, lo, hi)
        if found:
            print(f"found pattern {pattern}")
        else:
            print(f"did not find pattern {pattern}")
        sum += found

    return sum

def part2():
    sum = 0
    for pattern in patterns:
        sum += search_num(pattern, lo, hi)

    return sum

def search(pat, towels, lo=lo, hi=hi):
    if pat in towels:
        return True

    hi = min(hi, len(pat))
    # longest prefix first    v this +1 cost me a lot of time
    for pre in range(lo, hi + 1)[::-1]:
        prefix = pat[:pre]
        if prefix in towels:
            found = search(pat[pre:], towels)
            if found:
                return found

    return False


@cache
def search_num(pat, lo=lo, hi=hi) -> int:
    if len(pat) <= 0:
        return 1

    hi_ = min(hi, len(pat))
    found = 0
    for pre in range(lo, hi_ + 1):
        prefix = pat[:pre]
        if prefix in towels:
            found += search_num(pat[pre:])

    return found
