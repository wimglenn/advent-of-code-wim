"""
--- Day 23: Experimental Emergency Teleportation ---
https://adventofcode.com/2018/day/23
"""
import z3
from aocd import get_data
from parse import parse


def z3_abs(x):
    return z3.If(x >= 0, x, -x)


def z3_dist(x, y):
    return z3_abs(x[0] - y[0]) + z3_abs(x[1] - y[1]) + z3_abs(x[2] - y[2])


def dist(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])


data = get_data(year=2018, day=23)
template = "pos=<{:d},{:d},{:d}>, r={:d}"
bots = [parse(template, s).fixed for s in data.splitlines()]
x = z3.Int("x")
y = z3.Int("y")
z = z3.Int("z")
orig = (x, y, z)
cost_expr = x * 0
for *pos, r in bots:
    cost_expr += z3.If(z3_dist(orig, pos) <= r, 1, 0)
opt = z3.Optimize()
opt.maximize(cost_expr)
opt.minimize(z3_dist((0, 0, 0), (x, y, z)))
opt.check()
model = opt.model()
v = [model[c].as_long() for c in (x, y, z)]
print("best location:", v)
print("bots in range:", sum(1 for bot in bots if dist(bot[:3], v) < bot[3]))
print("distance from origin:", dist((0, 0, 0), v))
