"""
--- Day 6: Trash Compactor ---
https://adventofcode.com/2025/day/6
"""

from math import prod
from aocd import data

lines = data.splitlines()
d = [x.split() for x in lines]
dT = [list(x) for x in zip(*d)]
a = 0
for col in dT:
    op = prod if col.pop() == "*" else sum
    a += op([int(x) for x in col])
print("answer_a:", a)

ops = lines.pop().split()
lines = [" " + x for x in lines]
[L] = {len(x) for x in lines}
ns = []
b = 0
for i in reversed(range(L)):
    s = "".join([x[i] for x in lines]).strip()
    if s:
        ns.append(int(s))
    else:
        op = prod if ops.pop() == "*" else sum
        b += op(ns)
        ns.clear()
print("answer_b:", b)
