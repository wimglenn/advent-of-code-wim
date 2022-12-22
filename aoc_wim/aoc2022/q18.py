"""
--- Day 18: Boiling Boulders ---
https://adventofcode.com/2022/day/18
"""
from aocd import data
import networkx as nx
from itertools import product


def adj6(x, y, z):
    return [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]


cubes = {tuple(map(int, line.split(","))) for line in data.splitlines()}

graph = nx.Graph()
m = max(s for cube in cubes for s in cube) + 2
for c in product(range(-1, m), repeat=3):
    if c not in cubes:
        graph.add_node(c)

for c0 in graph:
    for c1 in adj6(*c0):
        if c1 in graph:
            graph.add_edge(c0, c1)

water = max(nx.connected_components(graph), key=len)

print("part a:", sum([c1 not in cubes for c0 in cubes for c1 in adj6(*c0)]))
print("part b:", sum([c in cubes for w in water for c in adj6(*w)]))
