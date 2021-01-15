"""
--- Day 25: Four-Dimensional Adventure ---
https://adventofcode.com/2018/day/25
"""
from itertools import combinations
import networkx as nx
from aocd import data

nodes = [tuple(int(n) for n in s.split(",")) for s in data.splitlines()]
graph = nx.Graph()
graph.add_nodes_from(nodes)
for node1, node2 in combinations(nodes, 2):
    if sum(abs(x - y) for x, y in zip(node1, node2)) <= 3:
        graph.add_edge(node1, node2)
print(nx.number_connected_components(graph))
