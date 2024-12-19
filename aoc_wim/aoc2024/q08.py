"""
--- Day 8: Resonant Collinearity ---
https://adventofcode.com/2024/day/8
"""
from aocd import data
from aoc_wim.zgrid import ZGrid
from collections import defaultdict
import itertools as it

grid = ZGrid(data)
d = defaultdict(list)
for z, g in grid.items():
    if g not in ".#":
        d[g].append(z)

a = set()
b = set()
for zs in d.values():
    for z1, z2 in it.combinations(zs, 2):
        b.update((z1, z2))
        for z, dz in ((z1, z1 - z2), (z2, z2 - z1)):
            ns = []
            while z + dz in grid:
                z += dz
                ns.append(z)
            a.update(ns[:1])
            b.update(ns)

print("answer_a:", len(a))
print("answer_b:", len(b))
