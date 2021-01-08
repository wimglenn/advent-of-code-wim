"""
--- Day 11: Hex Ed ---
https://adventofcode.com/2017/day/11
"""
from aoc_wim import zgrid
from aocd import data

z = d = dmax = 0
grid = zgrid.ZGrid({z: 1})
for step in data.split(","):
    z += zgrid.hexV[step]
    d = zgrid.hexagonal_distance(z)
    dmax = max(d, dmax)
    grid[z] = 1
    # grid.draw_hex(glyph=0, orientation="V", title=f" {d=}, {dmax=}")

print("part a:", d)
print("part b:", dmax)
