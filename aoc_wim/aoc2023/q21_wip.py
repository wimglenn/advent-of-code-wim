"""
--- Day 21: Step Counter ---
https://adventofcode.com/2023/day/21
"""
from aocd import data
from aoc_wim.zgrid import ZGrid
from aoc_wim.search import BFS


# __import__("logging").basicConfig(level=logging.DEBUG)


# data = """\
# ...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#.#....
# .##..S####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ..........."""


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


for n_steps in range(1, 26501365):
    bfs = BFS(adj,  max_depth=n_steps)
    bfs(state0)
    parity = n_steps % 2
    a = sum(v % 2 == parity for (z, Z), v in bfs.seen.items() if Z == 0)
    if n_steps == 64:
        o = {z: "O" for (z, Z), v in bfs.seen.items() if v % 2 == parity and Z == 0}
        o[z0] = "S"
        grid.draw(overlay=o, clear=1)
        input(f"answer_a {n_steps=}: {a}")
        break
