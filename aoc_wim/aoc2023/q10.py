"""
--- Day 10: Pipe Maze ---
https://adventofcode.com/2023/day/10
"""
import networkx as nx
from aocd import data

from aoc_wim.zgrid import ZGrid

data = data.translate(str.maketrans("-|F7LJ", "─│╭╮╰╯"))
grid = ZGrid(data)
s = grid.z("S")
graph = nx.Graph()
graph.add_nodes_from(grid)
horizontals = """\
── ─╯ ─╮ ╰─ ╰╯ ╰╮ ╭─ ╭╯ ╭╮
"""
verticals = """\
│ │ │ ╮ ╮ ╮ ╭ ╭ ╭
│ ╯ ╰ │ ╯ ╰ │ ╯ ╰
"""
verticals = [a + b for a, b in zip(*verticals.splitlines())][::2]

for z, v in grid.scan():
    vr = grid.get(z + 1, ".")
    vd = grid.get(z + 1j, ".")
    if v + vr in horizontals:
        graph.add_edge(z, z + 1)
    if v + vd in verticals:
        graph.add_edge(z, z + 1j)

dz_L = zip((-1j, 1, 1j, -1), "│╭╮ ─╮╯ │╰╯ ─╭╰".split())
s_join = {dz: grid.get(s + dz, ".") in L for dz, L in dz_L}
for dz, join in s_join.items():
    if join:
        graph.add_edge(s, s + dz)
match *s_join.values(),:
    case 0, 0, 1, 1: grid[s] = "╮"
    case 0, 1, 0, 1: grid[s] = "─"
    case 0, 1, 1, 0: grid[s] = "╭"
    case 1, 0, 0, 1: grid[s] = "╯"
    case 1, 0, 1, 0: grid[s] = "│"
    case 1, 1, 0, 0: grid[s] = "╰"

[loop] = [c for c in nx.connected_components(graph) if s in c]
print("answer_a:", len(loop) // 2)

interior = []
inside = False
for z, v in grid.scan():
    if z in loop and v in "│╭╮":
        inside = not inside
    if z not in loop and inside:
        interior.append(z)

print("answer_b:", len(interior))

# from termcolor import colored
# o = {z: colored(grid[z], "red") for z in loop}
# o[s] = colored("S", "blue")
# o |= {z: colored(grid[z], "green") for z in interior}
# grid.draw(overlay=o, hide_ax=True)
