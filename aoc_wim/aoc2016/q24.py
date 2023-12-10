"""
--- Day 24: Air Duct Spelunking ---
https://adventofcode.com/2016/day/24
"""
from itertools import combinations
from itertools import permutations

import networkx as nx
from aocd import data

from aoc_wim.zgrid import ZGrid

grid = ZGrid(data, on=".", off="#")
graph = grid.graph(extra="0123456789")
distances = {}
for a, b in combinations(graph.extra, 2):
    d = nx.shortest_path_length(graph, graph.extra[a], graph.extra[b])
    distances[a, b] = distances[b, a] = d


def shortest_path(part="a"):
    paths = {}
    for nodes in permutations(graph.extra.keys() - {"0"}):
        path = "0" + "".join(nodes)
        if part == "b":
            path += "0"
        paths[path] = sum(distances[a, b] for a, b in zip(path, path[1:]))
    return min(paths.values())


print("answer_a:", shortest_path(part="a"))
print("answer_b:", shortest_path(part="b"))
