"""
--- Day 11: Hex Ed ---
https://adventofcode.com/2017/day/11
"""
from aoc_wim import zgrid
from aocd import data

z = 0
grid = zgrid.ZGrid()
for step in data.split(","):
    z += zgrid.hexV[step]
    grid[z] = 1

print("part a:", zgrid.hexagonal_distance(z))
print("part b:", max([zgrid.hexagonal_distance(z) for z in grid]))
