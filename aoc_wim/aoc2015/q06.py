"""
--- Day 6: Probably a Fire Hazard ---
https://adventofcode.com/2015/day/6
"""
import numpy as np
from aocd import data


A = np.zeros((1000, 1000), dtype=bool)
B = np.zeros((1000, 1000), dtype=int)

for line in data.splitlines():
    action, p1, _, p2 = line.rsplit(None, 3)
    x1, y1 = [int(n) for n in p1.split(",")]
    x2, y2 = [int(n) for n in p2.split(",")]
    t = slice(x1, x2 + 1), slice(y1, y2 + 1)
    if action == "toggle":
        A[t] = ~A[t]
        B[t] += 2
    elif action == "turn on":
        A[t] = True
        B[t] += 1
    elif action == "turn off":
        A[t] = False
        B[t] -= 1
        B = B.clip(min=0)

print("part a:", A.sum())
print("part b:", B.sum())
