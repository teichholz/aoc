import helpers as h
import re
from functools import cmp_to_key
from collections import defaultdict


input = h.readday(5, 2024, example=False)

partial_order = defaultdict(list)

def parse():
    rules, updates = input.split("\n\n")
    rules, updates = [tuple(map(int, re.findall(r"\d{2}", rule))) for rule in rules.splitlines()], list(map(lambda lst: list(map(int, lst.split(","))), updates.splitlines()))
    return rules, updates


rules, updates = parse()
for (less, greaterThan) in rules:
    partial_order[less].append(greaterThan)


def is_less_or_equal(u, v, graph, visited=None):
    if visited is None:
        visited = set()
    if u == v:
        return True
    if u in visited:
        return False
    visited.add(u)
    for neighbor in graph[u]:
        # this does not work, neighbor == v would work
        if is_less_or_equal(neighbor, v, graph, visited):
            return True
    return False


def part1_not_working():
    """
    This doesn't work, i'm once again trying to be too smart here
    The input must not be a partial order, else this would have worked
    In fact, the ordering is not transitive, which causes the <= relation to work both ways
    Basically, if you represent the relation as a graph, there are cycles
    """

    sum = 0
    for update in updates:
        cur, *nums = update
        ordered = True
        for num in nums:
            if not is_less_or_equal(cur, num, partial_order):
                ordered = False
                break
            cur = num

        if ordered:
            sum += update[len(update) // 2]

    return sum


def part1():
    """
    Since we have a total order (except transitivity), this works
    """
    rules, updates = parse()
    cmp = cmp_to_key(lambda x, y: 1 - 2 * ((x, y) in rules))

    sum = 0
    for update in updates:
        srted = sorted(update, key=cmp)
        if update == srted:
            sum += update[len(update) // 2]

    return sum

def part2():
    rules, updates = parse()
    cmp = cmp_to_key(lambda x, y: 1 - 2 * ((x, y) in rules))

    sum = 0
    for update in updates:
        srted = sorted(update, key=cmp)
        if update != srted:
            sum += srted[len(update) // 2]

    return sum
