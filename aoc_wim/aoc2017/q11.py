"""
--- Day 11: Hex Ed ---
https://adventofcode.com/2017/day/11
"""
from aocd import data

from aoc_wim import zgrid

z = d = dmax = 0
grid = zgrid.ZGrid({z: 1})
for step in data.split(","):
    z += zgrid.hexV[step]
    d = zgrid.hexagonal_distance(z)
    dmax = max(d, dmax)
    grid[z] = 1
    # grid.draw_hex(glyph=0, orientation="V", title=f" {d=}, {dmax=}")

print("answer_a:", d)
print("answer_b:", dmax)
