"""
--- Day 6: Guard Gallivant ---
https://adventofcode.com/2024/day/6
"""
from aocd import data

from aoc_wim.zgrid import ZGrid


def walk(z, dz):
    n = 0
    path = {(z, dz): n}
    cyclic = False
    while z + dz in grid:
        while grid[z + dz] == "#":
            dz *= 1j
        z += dz
        n += 1
        if (z, dz) in path:
            cyclic = True
            break
        path[z, dz] = n
    return path, cyclic


grid = ZGrid(data)
path, _cyclic = walk(grid.z("^"), -1j)
path = list(path)
print("answer_a:", len(dict(path)))

b = 0
seen = {path[0][0]}
for (z0, dz0), (z1, _) in zip(path, path[1:]):
    if z1 not in seen:
        grid[z1] = "#"
        b += walk(z0, dz0)[1]
        grid[z1] = "."
        seen.add(z1)
print("answer_b:", b)
