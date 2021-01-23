"""
--- Day 20: A Regular Map ---
https://adventofcode.com/2018/day/20
"""
import networkx as nx
from aocd import data
from aoc_wim.zgrid import manhattan_distance
from aoc_wim.zgrid import ZGrid


def render(g):
    if isinstance(g, str):
        g = graph(g)
    xs = [int(z.real) for z in g.nodes]
    ys = [int(z.imag) for z in g.nodes]
    x0, x1 = min(xs) - 1, max(xs) + 2
    y0, y1 = min(ys) - 1, max(ys) + 2
    for y in range(y0, y1):
        line = ""
        for x in range(x0, x1):
            z = complex(x, y)
            if z == 0:
                line += "X"
            elif z in g.nodes:
                line += "."
            elif (z - 1, z + 1) in g.edges:
                line += "|"
            elif (z - 1j, z + 1j) in g.edges:
                line += "-"
            elif any(zn in g.nodes for zn in ZGrid.near(z, n=8)):
                line += "#"
            else:
                line += " "
        print(line)
    print()


def graph(data, z0=0):
    g = nx.Graph()
    g.add_node(z0)
    tails = [z0]
    stack = []
    for s in data[1:-1]:
        if s in "NSEW":
            dz = 2*getattr(ZGrid, s)
            tails[:] = [z + dz for z in tails]
            for z in tails:
                g.add_edge(z - dz, z)
        elif s == "(":
            stack.append(tails)
            new_tails = tails = tails.copy()
        elif s == "|":
            new_tails.extend(tails)
            tails = stack[-1].copy()
        elif s == ")":
            new_tails.extend(tails)
            stack.pop()
            tails = [*{}.fromkeys(new_tails)]
    return g


g = graph(data)

distances = {}
for z in sorted(g.nodes, key=manhattan_distance, reverse=True):
    if z in distances:
        continue
    path = nx.shortest_path(g, 0, z)
    for length, z in enumerate(path):
        distances[z] = length

print("part a:", max(distances.values()))
print("part b:", sum(d >= 1000 for d in distances.values()))
