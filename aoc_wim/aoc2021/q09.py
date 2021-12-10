"""
--- Day 9: Smoke Basin ---
https://adventofcode.com/2021/day/9
"""
from aocd import data
import networkx as nx
from aoc_wim.zgrid import ZGrid

grid = ZGrid(data)
basins = sorted(nx.connected_components(grid.graph(extra="012345678")), key=len)
print("part a:", sum(min([1 + int(grid[z]) for z in basin]) for basin in basins))
print("part b:", len(basins[-1]) * len(basins[-2]) * len(basins[-3]))
