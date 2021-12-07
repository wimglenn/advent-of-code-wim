"""
--- Day 7: The Treachery of Whales ---
https://adventofcode.com/2021/day/7
"""
from aocd import data
import numpy as np

A = np.array([int(n) for n in data.split(",")])
a = b = np.inf
for n in range(A.min(), A.max()):
    d = abs(A - n)
    a = min(a, d.sum())
    b = min(b, (d * (d + 1) // 2).sum())

print("part a:", a)
print("part b:", b)
