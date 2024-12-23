"""
--- Day 21: Step Counter ---
https://adventofcode.com/2023/day/21
"""
import json
import os
from aocd import data
from aoc_wim.search import BFS
from aoc_wim.zgrid import manhattan_distance
from aoc_wim.zgrid import ZGrid


grid = ZGrid(data, on=".", off="#")
z0 = grid.z("S")
grid[z0] = "."
plots = set(grid.bfs(z0=z0))


def step(n):
    parity = n % 2
    reachable = far = 0
    for z in plots:
        d = manhattan_distance(z, z0)
        if d > n:
            far += 1
        else:
            reachable += d % 2 == parity
    return reachable, far


def adj(state, h=grid.height, w=grid.width):
    z0, Z0 = state
    for z in grid.near(z0):
        if z in grid:
            Z = Z0
        else:
            qy, ry = divmod(z.imag, h)
            qx, rx = divmod(z.real, w)
            z = complex(rx, ry)
            Z = Z0 + complex(qx, qy)
        if (z, Z) not in bfs.seen and grid[z] == ".":
            yield z, Z


if "AOCD_EXTRA" not in os.environ:
    a, _ = step(64)
    print("answer_a:", a)
    N, rem = divmod(26501365, grid.width)
    r, f = step(rem)
    b = N*N*len(plots) + (2*N + 1)*r + N*f
    print("answer_b:", b)
else:
    extra = json.loads(os.environ["AOCD_EXTRA"])
    n_steps = extra["n_steps"]
    state0 = z0, 0
    bfs = BFS(adj,  max_depth=n_steps)
    bfs(state0)
    parity = n_steps % 2
    a = b = sum(v % 2 == parity for v in bfs.seen.values())
    print("answer_a:", a)
    print("answer_b:", b)
