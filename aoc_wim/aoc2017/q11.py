"""
--- Day 11: Hex Ed ---
https://adventofcode.com/2017/day/11
"""
from aoc_wim import hexgrid
from aocd import data

h = d = dmax = 0
for step in data.split(","):
    h += getattr(hexgrid, step)
    d = hexgrid.dist(h)
    dmax = max(d, dmax)

print("part a:", d)
print("part b:", dmax)
