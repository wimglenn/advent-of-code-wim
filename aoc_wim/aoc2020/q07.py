"""
--- Day 7: Handy Haversacks ---
https://adventofcode.com/2020/day/7
"""
from aocd import data
from collections import deque
import networkx as nx

g = nx.DiGraph()
for line in data.splitlines():
    left, right = line.split("s contain ")
    rights = right.split(", ")
    for right in rights:
        n, right = right.split(None, 1)
        right = right.rstrip("s.")
        n = 0 if n == "no" else int(n)
        g.add_edge(left, right, weight=n)

print("part a:", sum(nx.has_path(g, b, "shiny gold bag") for b in g.nodes) - 1)

b = -1
q = deque([(1, "shiny gold bag")])
while q:
    w, b0 = q.popleft()
    b += w
    q.extend((w * g[b0][b1]["weight"], b1) for b1 in g[b0])

print("part b:", b)
