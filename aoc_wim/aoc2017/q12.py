"""
--- Day 12: Digital Plumber ---
https://adventofcode.com/2017/day/12
"""
import networkx as nx
from aocd import data


graph = nx.Graph()
for line in data.replace(" <->", ",").splitlines():
    n0, *nodes = [int(n) for n in line.split(", ")]
    graph.add_node(n0)
    for node in nodes:
        graph.add_edge(n0, node)

[a] = [len(g) for g in nx.connected_components(graph) if 0 in g]
b = nx.number_connected_components(graph)

print("part a:", a)
print("part b:", b)
