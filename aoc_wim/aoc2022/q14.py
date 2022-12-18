"""
--- Day 14: Regolith Reservoir ---
https://adventofcode.com/2022/day/14
"""
import os
from aocd import data
from aoc_wim.zgrid import ZGrid
from aoc_wim.zgrid import zline
from aoc_wim.search import BFS

grid = ZGrid()
for line in data.splitlines():
    zs = [complex(*map(int, xy.split(","))) for xy in line.split(" -> ")]
    for z0, z1 in zip(zs, zs[1:]):
        for z in zline(z0, z1):
            grid[z] = "#"


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


def adj(z0):
    for dx in 0, -1, 1:
        z = z0 + dx + 1j
        if grid.get(z) != "#" and z.imag < ymax + 2:
            yield z


bfs = BFS(adj)
bfs(z_source)
b = len(bfs.seen)

print("part a:", a)
print("part b:", b)
