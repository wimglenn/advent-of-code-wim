"""
--- Day 6: Universal Orbit Map ---
https://adventofcode.com/2019/day/6
"""
import networkx as nx
from aocd import data


graph = nx.Graph(x.split(")") for x in data.splitlines())
print("part a:", sum(nx.shortest_path_length(graph, x, "COM") for x in graph))
if "YOU" in graph:
    print("part b:", nx.shortest_path_length(graph, "YOU", "SAN") - 2)
