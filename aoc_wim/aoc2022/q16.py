"""
--- Day 16: Proboscidea Volcanium ---
https://adventofcode.com/2022/day/16
"""
import itertools
from collections import defaultdict
from collections import deque

from aocd import data
from parse import parse


flow = {}
template = "Valve {} ha flow rate={:d}; tunnel lead to valve {}"
dist = defaultdict(lambda: float("inf"))
for line in data.splitlines():
    line = line.replace("s ", " ")
    v1, f, v2s = parse(template, line).fixed
    flow[v1] = f
    dist[v1, v1] = 0
    for v2 in v2s.split(", "):
        dist[v1, v2] = dist[v2, v1] = 1

# https://en.wikipedia.org/wiki/Floyd-Warshall_algorithm
for k, i, j in itertools.product(flow, repeat=3):
    dist[i, j] = min(dist[i, j], dist[i, k] + dist[k, j])

nonzero_flow = {k: v for k, v in flow.items() if v > 0}


def find_paths():
    # state vector:
    # current minute (int), current score (int), current valve (str), {valves_opened: minute} (dict)
    s0 = 0, 0, "AA", {}
    result = {}
    q = deque([s0])
    while q:
        t, s, pos, visited = q.popleft()
        k = frozenset(visited)
        if k not in result or result[k][1] < s:
            result[k] = visited, s
        for p in nonzero_flow:
            if p in visited:
                continue
            d = dist[pos, p]
            dt = 30 - t - d - 1
            if dt > 0:
                q.append((t + d + 1, s + flow[p] * dt, p, {**visited, p: t + d + 1}))
    return result.values()


paths = find_paths()
print("answer_a:", max(s for v, s in paths))

scores = {}
for path, _old_score in paths:
    # just prune the paths we already had for max_t=30
    path = {k: v for k, v in path.items() if v < 26}
    k = frozenset(path)
    # scores need to be recalculated
    score = sum((26 - t) * flow[k] for k, t in path.items())
    if scores.get(k, -1) < score:
        scores[k] = score

# order the paths with highest pressure relief first
visited = sorted(scores, key=scores.get, reverse=True)
b = 0
for i in range(len(visited)):
    v1 = visited[i]
    for j in range(i + 1, len(visited)):
        v2 = visited[j]
        if not v1 & v2:
            b = max(b, scores[v1] + scores[v2])
            break
    if scores[v1] * 2 <= b:
        # short-circuit because we can not possibly do any better now
        break

print("answer_b:", b)
