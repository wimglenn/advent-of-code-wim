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
    if right == "no other bags.":
        continue
    rights = right.split(", ")
    for right in rights:
        n, right = right.split(None, 1)
        right = right.rstrip("s.")
        g.add_edge(left, right, weight=int(n))

print("part a:", sum(nx.has_path(g, b, "shiny gold bag") for b in g.nodes) - 1)

b = -1
q = deque([(1, "shiny gold bag")])
while q:
    weight0, b0 = q.popleft()
    b += weight0
    for b1 in g[b0]:
        q.append((weight0 * g[b0][b1]["weight"], b1))

print("part b:", b)
