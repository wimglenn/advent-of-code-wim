"""
--- Day 1: Chronal Calibration ---
https://adventofcode.com/2018/day/1
"""
from itertools import cycle

from aocd import data


ns = [int(x) for x in data.split()]
print("part a:", sum(ns))

f = None
if len({n > 0 for n in ns}) == 2:
    f = 0
    seen = {f}
    for n in cycle(ns):
        f += n
        if f in seen:
            break
        seen.add(f)
print("part b:", f)
