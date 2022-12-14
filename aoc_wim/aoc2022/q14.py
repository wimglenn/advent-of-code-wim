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
    # where will piece of sand at s0 fall to (if anywhere)
    if s0.imag > ymax:
        raise Exception("flowing into the void")
    for dx in 0, -1, 1:
        if grid.get(s0 + 1j + dx, ".") not in "o#":
            return s1(s0 + 1j + dx)
    if grid.get(s0) == "o":
        raise Exception("flow is blocked")
    return s0


def flow(render=os.environ.get("AOC_DEBUG")):
    while True:
        try:
            s = s1(z_source)
        except Exception:
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
