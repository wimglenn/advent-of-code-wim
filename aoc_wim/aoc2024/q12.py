"""
--- Day 12: Garden Groups ---
https://adventofcode.com/2024/day/12
"""
from aocd import data
import networkx as nx
from aoc_wim.zgrid import ZGrid


grid = ZGrid(data)
graph = nx.Graph()
for z, g in grid.items():
    graph.add_node(z)
    if grid.get(z + 1) == g:
        graph.add_edge(z, z + 1)
    if grid.get(z + 1j) == g:
        graph.add_edge(z, z + 1j)

regions = [frozenset(r) for r in nx.connected_components(graph)]
for r in regions:
    grid.update(dict.fromkeys(r, r))  # label

area = {r: len(r) for r in regions}
perimeter = {r: sum(4 - len(graph[z]) for z in r) for r in regions}
n_sides = dict.fromkeys(regions, 0)
for z, r in grid.items():
    dzs = -1j, 1, 1j, -1, -1j
    for dz0, dz2 in zip(dzs, dzs[1:]):
        rs = [grid.get(z + dz) for dz in (dz0, dz0 + dz2, dz2)]
        n_sides[r] += r is not rs[0] and r is not rs[2]
        n_sides[r] += r is rs[0] is rs[2] and r is not rs[1]

print("answer_a:", sum(area[r] * perimeter[r] for r in regions))
print("answer_b:", sum(area[r] * n_sides[r] for r in regions))
