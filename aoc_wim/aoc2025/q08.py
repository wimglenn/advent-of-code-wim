"""
--- Day 8: Playground ---
https://adventofcode.com/2025/day/8
"""

import heapq
from aocd import data
from aocd import extra

ns = [int(x) for x in data.replace(",", " ").split()]
xs = ns[0::3]
ys = ns[1::3]
zs = ns[2::3]
[n] = {len(xs), len(ys), len(zs)}
min_heap = []
for i in range(n):
    for j in range(i + 1, n):
        dx = xs[i] - xs[j]
        dy = ys[i] - ys[j]
        dz = zs[i] - zs[j]
        d2 = dx**2 + dy**2 + dz**2
        heapq.heappush(min_heap, (d2, i, j))

components = {i: {i} for i in range(n)}
pair = 0
while True:
    _d2, i, j = heapq.heappop(min_heap)
    component = components[i] | components[j]
    for x in component:
        components[x] = component
    pair += 1
    if pair == extra.get("n_pairs", 1000):
        unique_components = {frozenset(x) for x in components.values()}
        component_lengths = [len(x) for x in unique_components]
        heapq.heapify(component_lengths)
        s0, s1, s2 = heapq.nlargest(3, component_lengths)
        print("answer_a:", s0 * s1 * s2)
    if len(component) == n:
        print("answer_b:", xs[i] * xs[j])
        break
