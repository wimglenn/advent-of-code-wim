"""
--- Day 9: Smoke Basin ---
https://adventofcode.com/2021/day/9
"""
from aocd import data
import networkx as nx
from aoc_wim.zgrid import ZGrid
import heapq
import math

g = ZGrid(data)
print("part a:", sum(1 + int(n) for z0, n in g.items() if all(n < g.get(z, 'z') for z in g.near(z0))))
basin_sizes = [len(b) for b in nx.connected_components(g.graph(extra="012345678"))]
print("part b:", math.prod(heapq.nlargest(3, basin_sizes)))
