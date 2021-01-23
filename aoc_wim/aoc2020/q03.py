"""
--- Day 3: Toboggan Trajectory ---
https://adventofcode.com/2020/day/3
"""
from math import prod
from aocd import data
from aoc_wim.zgrid import ZGrid

grid = ZGrid(data)
w, h = grid.width, grid.height
dzs = {}.fromkeys([1 + 1j, 3 + 1j, 5 + 1j, 7 + 1j, 1 + 2j], 0)
for dz in dzs:
    z = grid.top_left
    while z.imag < h:
        dzs[dz] += grid[complex(z.real % w, z.imag)] == "#"
        z += dz

print("part a:", dzs[3 + 1j])
print("part b:", prod(dzs.values()))
