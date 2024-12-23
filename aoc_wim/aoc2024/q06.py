"""
--- Day 6: Guard Gallivant ---
https://adventofcode.com/2024/day/6
"""
from aocd import data
from aoc_wim.zgrid import ZGrid


def walk():
    z, dz = z0, dz0
    seen = {(z, dz)}
    while z + dz in grid:
        while grid[z + dz] == "#":
            dz *= 1j
        z += dz
        if (z, dz) in seen:
            return seen, True
        seen.add((z, dz))
    return seen, False


grid = ZGrid(data)
z0, dz0 = grid.z("^"), -1j
seen, _ = walk()
path = dict(seen)
print("answer_a:", len(path))

b = 0
path.pop(z0)
for z in path:
    grid[z] = "#"
    b += walk()[1]
    grid[z] = "."
print("answer_b:", b)
