from collections import defaultdict
from helpers import readdaylines, profiler

lines = list(map(int, readdaylines(22, 2024, example=False)))


def generate(secret: int) -> int:
    # 64 == 2 ** 6
    a = mix_and_prune(secret * 64, secret)
    # 32 == 2 ** 5
    b = mix_and_prune(a // 32, a)
    # 2048 == 2 ** 11
    c = mix_and_prune(b * 2048, b)

    return c

def mix_and_prune(secret, prev):
    mixed = secret ^ prev
    # 16777216 == 2 ** 24
    pruned = mixed % 16777216
    return pruned

@profiler
def part1():
    sum = 0
    for initial_secret in lines:
        cur = initial_secret
        for _ in range(2000):
            cur = generate(cur)
        sum += cur

    return sum

@profiler
def part2():
    most_global = defaultdict(int)

    for initial_secret in lines:
        cur = initial_secret
        prices = [cur % 10]

        for _ in range(2000):
            cur = generate(cur)
            prices.append(cur % 10)

        changes = []
        for i, price in enumerate(prices[1:], 1):
            changes.append(price - prices[i - 1])

        seen = set()
        for i in range(len(changes) - 3):
            seq = changes[i:i + 4]
            price = prices[i + 3 + 1]
            combined = tuple(seq)
            if combined not in seen:
                most_global[combined] += price

    return max(most_global.values()), most_global
