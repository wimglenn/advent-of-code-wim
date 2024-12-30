"""
--- Day 23: LAN Party ---
https://adventofcode.com/2024/day/23
"""
from aocd import data
import networkx as nx
import itertools as it


graph = nx.Graph(x.split("-") for x in data.split())
triples = set()
for t in graph:
    if t.startswith("t"):
        for u, v in it.combinations(graph[t], 2):
            if (u, v) in graph.edges():
                triples.add(frozenset([t, u, v]))
print("answer_a:", len(triples))

clique = max(nx.find_cliques(graph), key=len)
print("answer_b:", ",".join(sorted(clique)))
