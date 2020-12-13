"""
--- Day 2: Inventory Management System ---
https://adventofcode.com/2018/day/2
"""
from collections import Counter
from itertools import combinations

from aocd import data


counters = [Counter(s) for s in data.split()]
doubles = sum(1 for c in counters if 2 in c.values())
triples = sum(1 for c in counters if 3 in c.values())
print("part a:", doubles * triples)

for a, b in combinations(data.split(), 2):
    s = "".join([x for x, y in zip(a, b) if x == y])
    if len(s) == len(a) - 1:
        print("part b:", s)
        break
