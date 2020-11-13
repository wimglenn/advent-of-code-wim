"""
--- Day 24: It Hangs in the Balance ---
https://adventofcode.com/2015/day/24
"""
from collections import Counter
from itertools import combinations
from math import prod

from aocd import data

from aoc_wim.stuff import subset_sum


def parsed(data, n_groups):
    vals = [int(n) for n in data.strip().split()]
    total = sum(vals)
    if total % n_groups != 0:
        raise Exception
    return vals, total // n_groups


def bag_sub(list_big, sublist):
    counter = Counter(sublist)
    result = []
    for k in list_big:
        counter[k] -= 1
        if counter[k] < 0:
            result.append(k)
    return result


def partitions(vals, target):
    for group in subset_sum(vals, target):
        rem = bag_sub(vals, group)
        groups = partitions(rem, target) if sum(rem) > target else (rem,)
        yield from ((group, group_) for group_ in groups)


def get_shortest_sums(vals, target):
    results = []
    for i in range(len(vals)):
        for comb in combinations(vals, i):
            if sum(comb) == target:
                results.append(comb)
        if results:
            return results
        del results[:]


def solve(data, n_groups):
    vals, target = parsed(data, n_groups=n_groups)
    group1s = get_shortest_sums(vals, target)
    group1s.sort(key=prod)

    for group1 in group1s:
        rem = bag_sub(vals, group1)
        gen = partitions(rem, target)
        try:
            next(gen)
        except StopIteration:
            continue
        return prod(group1)


print(solve(data, n_groups=3))
print(solve(data, n_groups=4))
