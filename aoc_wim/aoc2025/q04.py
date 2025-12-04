"""
--- Day 4: Printing Department ---
https://adventofcode.com/2025/day/4
"""

from aocd import data
from aoc_wim.zgrid import ZGrid

grid = ZGrid(data)
zs = [z for z in grid.z("@", 0) if grid.count_near(z, "@", n=8) < 4]
a = b = len(zs)
print("answer_a:", a)

while zs:
    grid.update(dict.fromkeys(zs, "x"))
    zs = [z for z in grid.z("@", 0) if grid.count_near(z, "@", n=8) < 4]
    b += len(zs)
print("answer_b:", b)
