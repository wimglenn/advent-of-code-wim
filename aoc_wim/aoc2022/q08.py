"""
--- Day 8: Treetop Tree House ---
https://adventofcode.com/2022/day/8
"""
from aocd import data
from aoc_wim.zgrid import ZGrid, zrange

grid = ZGrid(data, transform=int)
h, w = grid.height, grid.width
a = 2*h + 2*w - 4  # perimeter trees are always visible
b = 0
for z0 in zrange(complex(1, 1), complex(w - 1, h - 1)):  # interior trees
    n = grid[z0]
    vis = False  # visibility from exterior
    ss = 1  # scenic score
    for dz in 1, -1, 1j, -1j:
        z = z0
        s = 0
        while True:
            z += dz
            if z not in grid:
                vis = True
                break
            s += 1
            if grid[z] >= n:
                break
        ss *= s
    a += vis
    b = max(b, ss)

print("part a:", a)
print("part b:", b)
