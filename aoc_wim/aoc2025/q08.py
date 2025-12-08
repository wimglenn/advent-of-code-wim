"""
--- Day 8: Playground ---
https://adventofcode.com/2025/day/8
"""

from aocd import data
from aocd import extra

ns = [int(x) for x in data.replace(",", " ").split()]
xs = ns[0::3]
ys = ns[1::3]
zs = ns[2::3]
[n] = {len(xs), len(ys), len(zs)}
d2 = {}
for i in range(n):
    for j in range(i + 1, n):
        dx = xs[i] - xs[j]
        dy = ys[i] - ys[j]
        dz = zs[i] - zs[j]
        d2[frozenset([i, j])] = dx**2 + dy**2 + dz**2
d2 = {k: d2[k] for k in sorted(d2, key=d2.get, reverse=True)}

components = {i: {i} for i in range(n)}
pair = 0
while True:
    (i, j), _d = d2.popitem()
    component = components[i] | components[j]
    for x in component:
        components[x] = component
    pair += 1
    if pair == extra.get("n_pairs", 1000):
        unique_components = {frozenset(x) for x in components.values()}
        sizes = sorted([len(x) for x in unique_components], reverse=True)
        print("answer_a:", sizes[0] * sizes[1] * sizes[2])
    if len(component) == n:
        print("answer_b:", xs[i] * xs[j])
        break
