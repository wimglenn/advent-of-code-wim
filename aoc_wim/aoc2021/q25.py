"""
--- Day 25: Sea Cucumber ---
https://adventofcode.com/2021/day/25
"""
from aocd import data
from aoc_wim.zgrid import ZGrid


def evolve(g):
    moved_right = {}
    for z, zr, _ in z_zr_zd:
        if g[z] == ">" and g[zr] == ".":
            moved_right[z], moved_right[zr] = g[zr], g[z]
    g.update(moved_right)
    moved_down = {}
    for z, _, zd in z_zr_zd:
        if g[z] == "v" and g[zd] == ".":
            moved_down[z], moved_down[zd] = g[zd], g[z]
    g.update(moved_down)
    return len(moved_right) + len(moved_down)


grid = ZGrid(data)
H, W = grid.height, grid.width
z_zr_zd = [
    (complex(x, y), complex((x + 1) % W, y), complex(x, (y + 1) % H))
    for x in range(W)
    for y in range(H)
]
n = 0
while evolve(grid):
    n += 1

print(n + 1)
