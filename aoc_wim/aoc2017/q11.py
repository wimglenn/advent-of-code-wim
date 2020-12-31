"""
--- Day 11: Hex Ed ---
https://adventofcode.com/2017/day/11
"""
from aoc_wim import hexgrid
from aocd import data

# rotate to convert flat topped hexagon orientation into pointy topped
# see https://www.redblobgames.com/grids/hexagons/#basics
rot = {
    "n": hexgrid.nw,
    "nw": hexgrid.w,
    "sw": hexgrid.sw,
    "s": hexgrid.se,
    "se": hexgrid.e,
    "ne": hexgrid.ne,
}

h = hexgrid.o
d = dmax = hexgrid.dist(h)
for step in data.split(","):
    h += rot[step]
    d = hexgrid.dist(h)
    dmax = max(d, dmax)

print("part a:", d)
print("part b:", dmax)
