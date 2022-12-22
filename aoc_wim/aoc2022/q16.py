"""
--- Day 16: Proboscidea Volcanium ---
https://adventofcode.com/2022/day/16
"""
from aocd import data
from collections import deque
import networkx as nx
import itertools
import heapq


valves = {}
graph = nx.Graph()
for line in data.splitlines():
    parts = line.split()
    f = int(parts[4].split("=")[1][:-1])
    v, *vs = [x.rstrip(",") for x in parts if x.rstrip(",").isupper()]
    if f > 0:
        valves[v] = f
    for t in vs:
        graph.add_edge(v, t)

dist = {}
for p1, p2 in itertools.combinations(["AA", *valves], 2):
    dist[p1, p2] = dist[p2, p1] = nx.shortest_path_length(graph, p1, p2)


def go(dont_visit=(), max_visits=float("inf")):
    # state vector:
    # current minute (int), current position (str), valves opened: minute (dict)
    s0 = 0, "AA", {}
    result = []
    q = deque([s0])
    while q:
        m, pos, v = q.popleft()
        if m >= M:
            result.append(v)
            continue
        candidates = [p for p in valves if p not in v and p not in dont_visit]
        if not candidates or len(v) >= max_visits:
            result.append(v)
            continue
        for p in candidates:
            d = dist[pos, p]
            if m + d + 1 > M:
                q.append((M, p, v))
            else:
                q.append((m + d + 1, p, {**v, p: m + d + 1}))
    return result


def score(end):
    return sum((M - v) * valves[k] for k, v in end.items())


M = 30
paths = go()
print("part a:", max(score(p) for p in paths))

M = 26
b = 0
your_paths = go(max_visits=len(valves) // 2)
for your_path in heapq.nlargest(20, your_paths, key=score):
    your_score = score(your_path)
    ele_paths = go(dont_visit=your_path)
    for ele_path in ele_paths:
        ele_score = score(ele_path)
        b = max(b, your_score + ele_score)
print("part b:", b)
