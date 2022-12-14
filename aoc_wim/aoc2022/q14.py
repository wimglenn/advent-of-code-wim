"""
--- Day 14: Regolith Reservoir ---
https://adventofcode.com/2022/day/14
"""
import os
from aocd import data
from aoc_wim.zgrid import ZGrid

grid = ZGrid()
for line in data.splitlines():
    z0 = None
    for xy in line.split(" -> "):
        z1 = complex(*map(int, xy.split(",")))
        if z0 is not None:
            dz = z1 - z0
            dz /= abs(dz)
            while z0 != z1:
                grid[z0] = "#"
                z0 += dz
        z0 = z1
        grid[z1] = "#"


def s1(s0):
    # how will piece of sand at s0 come to rest (if anywhere)
    path = [s0]
    while path[-1].imag <= ymax:
        for dx in 0, -1, 1:
            if path[-1] + 1j + dx not in grid:
                path.append(path[-1] + 1j + dx)
                break
        else:
            break
    return path


def flow(render=os.environ.get("AOC_DEBUG")):
    path = []
    while True:
        path = s1(path[-1] if path else z_source)
        s = path.pop()
        if s.imag > ymax or s in grid:  # flowing into void, or flow is blocked
            return
        grid[s] = "o"
        if render:
            grid.draw(overlay={z_source: "+", s: "O"}, clear=True, title=__doc__)


z_source = 500
ymax = int(grid.bottom_right.imag)
flow()
a = grid.count("o")

# add in a floor to the grid
ymax += 2
for x in range(-ymax, ymax + 1):
    grid[z_source + x + ymax * 1j] = "#"

flow()
b = grid.count("o")

print("part a:", a)
print("part b:", b)
