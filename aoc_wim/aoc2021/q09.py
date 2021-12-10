"""
--- Day 9: Smoke Basin ---
https://adventofcode.com/2021/day/9
"""
from aocd import data
import networkx as nx
from aoc_wim.zgrid import ZGrid

g = ZGrid(data)
bs = sorted(nx.connected_components(g.graph(extra="012345678")), key=len)
print("part a:", sum(min([1 + int(g[z]) for z in b]) for b in bs))
print("part b:", len(bs[-1]) * len(bs[-2]) * len(bs[-3]))
