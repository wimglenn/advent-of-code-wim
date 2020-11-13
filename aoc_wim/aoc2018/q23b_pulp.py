"""
--- Day 23: Experimental Emergency Teleportation ---
https://adventofcode.com/2018/day/23
"""
from itertools import product

import pulp
from aocd import data
from parse import parse


pvar = pulp.LpVariable
template = "pos=<{:d},{:d},{:d}>, r={:d}"
bots = [parse(template, s).fixed for s in data.splitlines()]
prob = pulp.LpProblem("problem", pulp.LpMaximize)
cs = [pvar(f"c{i}", lowBound=0, upBound=1, cat="Integer") for i in range(len(bots))]
x = pvar("x")
y = pvar("y")
z = pvar("z")
n = pvar("n")

prob += n
prob += n == sum(cs)
for i, (xi, yi, zi, r) in enumerate(bots):
    ci = cs[i]
    for s in product([-1, 1], repeat=3):
        d = s[0] * (x - xi) + s[1] * (y - yi) + s[2] * (z - zi)
        prob += d <= r + (1 - ci) * 10 ** 10

status = prob.solve()
assert pulp.LpStatus[status] == "Optimal"
v = [int(pulp.value(c)) for c in (x, y, z)]
print("best location:", v)
print("bots in range:", int(pulp.value(n)))
print("distance from origin:", sum([abs(c) for c in v]))
