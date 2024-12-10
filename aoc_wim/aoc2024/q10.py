"""
--- Day 10: Hoof It ---
https://adventofcode.com/2024/day/10
"""
from aocd import data
import networkx as nx
from aoc_wim.zgrid import ZGrid

grid = ZGrid(data, transform=int)
graph = nx.DiGraph()
for z0, n in grid.items():
    for z in grid.near(z0):
        if grid.get(z, n) - n == 1:
            graph.add_edge(z0, z)

a = b = 0
for head in grid.z(0, first=False):
    for peak in grid.z(9, first=False):
        paths = list(nx.all_simple_paths(graph, head, peak))
        a += bool(paths)
        b += len(paths)

print("answer_a:", a)
print("answer_b:", b)
