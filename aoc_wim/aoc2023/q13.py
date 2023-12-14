"""
--- Day 13: Point of Incidence ---
https://adventofcode.com/2023/day/13
"""
from aocd import data

data = data.translate(str.maketrans("#.", "10"))
a = b = 0
for chunk in data.split("\n\n"):
    nr = [int(line, 2) for line in chunk.splitlines()]
    nc = [int("".join(line), 2) for line in zip(*chunk.splitlines())]
    for ns, f in zip([nr, nc], [100, 1]):
        for i in range(len(ns)):
            p = sum([(x ^ y).bit_count() for x, y in zip(ns[:i][::-1], ns[i:])])
            a += f * i * (p == 0)
            b += f * i * (p == 1)

print("answer_a:", a)
print("answer_b:", b)
