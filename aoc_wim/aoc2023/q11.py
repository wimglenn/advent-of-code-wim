"""
--- Day 11: Cosmic Expansion ---
https://adventofcode.com/2023/day/11
"""
from itertools import combinations

from aocd import data

from aoc_wim.zgrid import manhattan_distance
from aoc_wim.zgrid import ZGrid

grid = ZGrid(data)
h, w = grid.height, grid.width
gs = grid.z("#", first=False)
g_cols = {g.real for g in gs}
g_rows = {g.imag for g in gs}
empty_cols = [i for i in range(w) if i not in g_cols]
empty_rows = [i for i in range(h) if i not in g_rows]

# expansion factor for part b
f = 1_000_000
if len(gs) == 9:
    # 9 galaxies for the example data
    # use a smaller expansion factor
    f = 100

a = b = 0
for g0, g1 in combinations(gs, 2):
    d = manhattan_distance(g0, g1)
    c01 = range(*sorted([int(g0.real), int(g1.real)]))
    r01 = range(*sorted([int(g0.imag), int(g1.imag)]))
    c = sum(1 for c in empty_cols if c in c01)
    r = sum(1 for r in empty_rows if r in r01)
    a += d + c + r
    b += d + (c + r) * (f - 1)

print("answer_a:", a)
print("answer_b:", b)
