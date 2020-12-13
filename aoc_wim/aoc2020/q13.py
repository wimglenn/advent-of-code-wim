"""
--- Day 13: Shuttle Search ---
https://adventofcode.com/2020/day/13
"""
import math
from aocd import data

t0, table = data.splitlines()
t0 = int(t0)
table = {-i: int(m) for i, m in enumerate(table.split(",")) if m != "x"}
bs, buses = zip(*table.items())
wait, bus = min([(-t0 % b, b) for b in buses])
print("part a:", wait * bus)

# chinese remainder theorem...
M = math.lcm(*buses)
ns = [M // m for m in buses]
nis = [pow(n, -1, m) for n, m in zip(ns, buses)]
t = sum(b*n*ni for b, n, ni in zip(bs, ns, nis)) % M
print("part b:", t)
