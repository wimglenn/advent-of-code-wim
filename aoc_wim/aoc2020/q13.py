"""
--- Day 13: Shuttle Search ---
https://adventofcode.com/2020/day/13
"""
import math
from aocd import data

bus, table = data.splitlines()
bus = int(bus)
table = {-i: int(m) for i, m in enumerate(table.split(",")) if m != "x"}
earliest = min(table.values(), key=lambda v: -bus % v)
print("part a:", earliest * (-bus % earliest))

# chinese remainder theorem...
M = math.lcm(*table.values())
ns = [M // m for m in table.values()]
nis = [pow(n, -1, m) for n, m in zip(ns, table.values())]
t = sum(b*n*ni for b, n, ni in zip(table, ns, nis)) % M
print("part b:", t)
