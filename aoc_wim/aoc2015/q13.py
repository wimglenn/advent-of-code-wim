"""
--- Day 13: Knights of the Dinner Table ---
https://adventofcode.com/2015/day/13
"""
from collections import defaultdict
from itertools import permutations

from aocd import data


def parsed(data, extra_name=None):
    d = defaultdict(int)
    names = {extra_name} - {None}
    for line in data.splitlines():
        words = line.split()
        name0 = words[0]
        name1 = words[-1].rstrip(".")
        n = {"gain": 1, "lose": -1}[words[2]] * int(words[3])
        d[(name0, name1)] = n
        names |= {name0, name1}
    return names, d


def get_best_plan(data, extra_name=None):
    names, d = parsed(data, extra_name)
    n = len(names)
    plans = permutations(names)
    happiness = {}
    for plan in plans:
        total = 0
        for i in range(n):
            person = plan[i]
            left = plan[(i - 1) % n]
            right = plan[(i + 1) % n]
            total += d[(person, left)]
            total += d[(person, right)]
        happiness[plan] = total
    return max(happiness.values())


print(get_best_plan(data))
print(get_best_plan(data, extra_name="wim"))
