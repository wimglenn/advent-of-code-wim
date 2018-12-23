from itertools import product
from aocd import data
from parse import parse
import pulp


template = "pos=<{:d},{:d},{:d}>, r={:d}"
bots = [parse(template, s).fixed for s in data.splitlines()]
N = len(bots)

prob = pulp.LpProblem("problem", pulp.LpMaximize)

cs = [pulp.LpVariable(f"c{i}", lowBound=0, upBound=1, cat="Integer") for i in range(N)]
x = pulp.LpVariable("x")
y = pulp.LpVariable("y")
z = pulp.LpVariable("z")
n = pulp.LpVariable("n")

prob += n
prob += n == sum(cs)
for i, (xi, yi, zi, r) in enumerate(bots):
    ci = cs[i]
    for s in product([-1, 1], repeat=3):
        prob += (s[0] * (x - xi) + s[1] * (y - yi) + s[2] * (z - zi)) <= r + (
            1 - ci
        ) * 10**10

status = prob.solve()
assert pulp.LpStatus[status] == "Optimal"
v = [int(pulp.value(c)) for c in (x, y, z)]
print("best location:", v)
print("bots in range:", int(pulp.value(n)))
print("distance from origin:", sum([abs(c) for c in v]))
