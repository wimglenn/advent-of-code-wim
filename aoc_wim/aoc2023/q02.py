"""
--- Day 2: Cube Conundrum ---
https://adventofcode.com/2023/day/2
"""
from collections import Counter
from math import prod

from aocd import data

bag = Counter("rgb"*12 + "g" + "bb")
a = b = 0
for line in data.replace(";", ",").splitlines():
    g, line = line.removeprefix("Game").split(":")
    d = Counter()
    for n_c in line.split(","):
        n, c = n_c.split()
        d[c[0]] = max(d[c[0]], int(n))
    a += int(g) * (d <= bag)
    b += prod(d.values())

print("answer_a:", a)
print("answer_b:", b)
