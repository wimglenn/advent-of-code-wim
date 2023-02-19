"""
--- Day 16: Proboscidea Volcanium ---
https://adventofcode.com/2022/day/16
"""
from aocd import data
from collections import defaultdict
from collections import deque
import itertools
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


def go(max_t=30):
    # state vector:
    # current minute (int), current position (str), {valves_opened: minute} (dict)
    s0 = 0, "AA", {}
    result = []
    q = deque([s0])
    while q:
        t, pos, visited = q.popleft()
        end = True
        for p in nonzero_flow:
            if p in visited:
                continue
            d = dist[pos, p]
            if t + d + 1 < max_t:
                end = False
                q.append((t + d + 1, p, {**visited, p: t + d + 1}))
        if end:
            result.append(visited)
    return result


def score(visited, max_t=30):
    return sum((max_t - t) * flow[k] for k, t in visited.items())


paths = go()
print("part a:", max(score(p) for p in paths))

scores = {}
for path in paths:
    # just prune the paths we already had for max_t=30
    path = {k: v for k, v in path.items() if v < 26}
    vs = frozenset(path)
    s = score(path, max_t=26)
    if scores.get(vs, -1) < s:
        scores[vs] = s

# order the paths with highest pressure relief first
visited = sorted(scores, key=scores.get, reverse=True)
pressures = [scores[k] for k in visited]

b = 0
for i in range(len(visited)):
    v1 = visited[i]
    p1 = pressures[i]
    for j in range(i + 1, len(visited)):
        v2 = visited[j]
        p2 = pressures[j]
        if not v1 & v2:
            b = max(b, p1 + p2)
            break
    if p1 * 2 <= b:
        # short-circuit because we can not possibly do any better now
        break

print("part b:", b)
