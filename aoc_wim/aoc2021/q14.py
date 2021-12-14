"""
--- Day 14: Extended Polymerization ---
https://adventofcode.com/2021/day/14
"""
from collections import Counter
from aocd import data

polymer, rules = data.split("\n\n")
tr = dict(r.split(" -> ") for r in rules.splitlines())
c0 = Counter(x + y for x, y in zip(polymer, polymer[1:]))
c = Counter(polymer)
for i in range(40):
    if i == 10:
        print("part a:", max(c.values()) - min(c.values()))
    c1 = Counter()
    for xy, n in c0.items():
        c1[xy[0] + tr[xy]] += n
        c1[tr[xy] + xy[1]] += n
        c += {tr[xy]: n}
    c0 = c1
print("part b:", max(c.values()) - min(c.values()))
