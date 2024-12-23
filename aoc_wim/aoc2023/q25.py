"""
--- Day 25: Snowverload ---
https://adventofcode.com/2023/day/25
"""
from aocd import data
import networkx as nx


graph = nx.Graph()
for line in data.replace(":", "").splitlines():
    left, *rights = line.split()
    for right in rights:
        graph.add_edge(left, right)

ebc = nx.edge_betweenness_centrality(graph)
for i in range(3):
    edge = max(ebc, key=ebc.get)
    graph.remove_edge(*edge)
    del ebc[edge]

comp1, comp2 = nx.connected_components(graph)
print("answer_a:", len(comp1) * len(comp2))
