"""
--- Day 21: Step Counter ---
https://adventofcode.com/2023/day/21
"""
import json
import math
import os
from aocd import data
from aoc_wim.zgrid import ZGrid
from aoc_wim.search import BFS


data = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


def explode(data, n=999):
    lines = [x*n for x in data.replace("S", ".").splitlines()] * n
    m = len(lines)//2
    lines[m] = lines[m][:m] + "S" + lines[m][m+1:]
    result = "\n".join(lines)
    return result


data = explode(data)
grid = ZGrid(data)
c = math.isqrt(len(grid.d))//2
z0 = c + c*1j
grid[z0] = "."


def adj(z0):
    for z in grid.near(z0):
        if z not in bfs.seen and grid.get(z) == ".":
            yield z


# grid.draw(overlay={z0: "S"}, clear=True)
# input("initial")
for n_steps_a in [6, 10, 50, 100, 500, 1000, 5000]:
    bfs = BFS(adj,  max_depth=n_steps_a)
    bfs(z0)
    parity = n_steps_a % 2
    overlay = {z: "S" for z, depth in bfs.seen.items() if depth % 2 == parity}
    # grid.draw(overlay=overlay, clear=True)
    print(f"answer_a ({n_steps_a}): {len(overlay)}")
