"""
--- Day 24: Blizzard Basin ---
https://adventofcode.com/2022/day/24
"""
import networkx as nx
from aocd import data
from aoc_wim.zgrid import ZGrid
from itertools import count


grid = ZGrid(data)
grid.offset(-1-1j)
h = grid.height - 2
w = grid.width - 2
min_depth = h + w

bu = grid.z("^", first=False)
br = grid.z(">", first=False)
bd = grid.z("v", first=False)
bl = grid.z("<", first=False)


empty = ZGrid({z: ".#"[g == "#"] for z, g in grid.items()})
z_start = -1j
z_end = w - 1 + h * 1j


rep = dict.fromkeys("^>v<", "2")
rep["2"] = "3"
rep["3"] = "4"


def bliz(t):
    g = ZGrid(empty)
    u_y = [(int(z.imag) - t) % h for z in bu]
    r_x = [(int(z.real) + t) % w for z in br]
    d_y = [(int(z.imag) + t) % h for z in bd]
    l_x = [(int(z.real) - t) % w for z in bl]
    u = [z.real + 1j * y for z, y in zip(bu, u_y)]
    r = [x + 1j * z.imag for z, x in zip(br, r_x)]
    d = [z.real + 1j * y for z, y in zip(bd, d_y)]
    l = [x + 1j * z.imag for z, x in zip(bl, l_x)]
    g.update(dict.fromkeys(u, "^"))
    g.update({z: rep.get(g[z], ">") for z in r})
    g.update({z: rep.get(g[z], "v") for z in d})
    g.update({z: rep.get(g[z], "<") for z in l})
    return g


def add_edges(i, g_prev, g):
    graph.add_node((i, z_start))
    graph.add_node((i, z_end))
    for z0 in g.z(".", first=False):
        for z in g_prev.near(z0, n=5):
            if g_prev.get(z) == ".":
                graph.add_edge((i - 1, z), (i, z0))


graph = nx.DiGraph()
graph.add_node((0, z_start))
g_prev = bliz(0)
a = b0 = b = None
for i in count(1):
    g = bliz(i)
    add_edges(i, g_prev, g)
    g_prev = g
    if i < min_depth:
        continue
    if a is None and nx.has_path(graph, (0, z_start), (i, z_end)):
        a = i
    if a and b0 is None and nx.has_path(graph, (a, z_end), (i, z_start)):
        b0 = i - a
    if a and b0 and nx.has_path(graph, (a + b0, z_start), (i, z_end)):
        b = i
        break

print("part a:", a)
print("part b:", b)
