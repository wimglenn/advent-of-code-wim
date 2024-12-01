"""
--- Day 21: Step Counter ---
https://adventofcode.com/2023/day/21
"""
import json
import os
from aocd import data
from aoc_wim.zgrid import ZGrid
from aoc_wim.search import BFS


grid = ZGrid(data)
z0 = grid.z("S")
grid[z0] = "."
state0 = z0, 0
h = grid.height
w = grid.width


def adj(state):
    z0, Z0 = state
    for z in grid.near(z0):
        if z.imag < 0:
            z += h*1j
            Z = Z0 - 1j
        elif z.imag >= h:
            z -= h*1j
            Z = Z0 + 1j
        elif z.real < 0:
            z += w
            Z = Z0 - 1
        elif z.real >= w:
            z -= w
            Z = Z0 + 1
        else:
            Z = Z0
        if (z, Z) in bfs.seen:
            continue
        if grid[z] == ".":
            yield z, Z


extra = json.loads(os.environ.get("AOCD_EXTRA", "{}"))
n_steps_a = extra.get("n_steps", 64)
bfs = BFS(adj,  max_depth=n_steps_a)
bfs(state0)
parity = n_steps_a % 2
a = b = sum(v % 2 == parity for v in bfs.seen.values())
print("answer_a:", a)
print("answer_a:", b)

n_steps_b = extra.get("n_steps", 26501365)
