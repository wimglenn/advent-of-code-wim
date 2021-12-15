"""
--- Day 12: Passage Pathing ---
https://adventofcode.com/2021/day/12
"""
from aocd import data
from collections import defaultdict
from collections import deque


caves = defaultdict(set)
for line in data.splitlines():
    x, y = line.split("-")
    caves[x].add(y)
    caves[y].add(x)


def get_neighbors_a(here, visited):
    return [c for c in caves[here] if c.isupper() or c not in visited]


def get_neighbors_b(here, visited):
    if any(v > 1 for k, v in visited.items() if not k.isupper()):
        # we've already visited a small cave twice
        return get_neighbors_a(here, visited)
    return [n for n in caves[here] if n != "start"]


def n_paths(part):
    get_neighbors = get_neighbors_a if part == "a" else get_neighbors_b
    result = 0
    q = deque([(["start"], {"start": 1})])
    while q:
        path, visited = q.pop()
        here = path[-1]
        if here == "end":
            result += 1
            continue
        neighbors = get_neighbors(here, visited)
        q.extend([(path + [n], {**visited, n: visited.get(n, 0) + 1}) for n in neighbors])
    return result


print("part a:", n_paths("a"))
print("part b:", n_paths("b"))
