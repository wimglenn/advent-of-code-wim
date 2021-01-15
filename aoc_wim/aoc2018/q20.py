"""
--- Day 20: A Regular Map ---
https://adventofcode.com/2018/day/20
"""
import networkx as nx
from aocd import data


# TODO: refactor to use zgrid
steps = dict(zip("NSEW", [-2j, 2j, 2, -2]))
dzs = [
    -1j-1, -1j, -1j+1,
    -1,             1,
    +1j-1, +1j, +1j+1,
]


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
            elif any(z + dz in g.nodes for dz in dzs):
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
        if s in steps:
            dz = steps[s]
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
distances = [nx.shortest_path_length(g, 0, x) for x in g.nodes]

print("part a:", max(distances))
print("part b:", sum(1 for d in distances if d >= 1000))
