"""
--- Day 1: The Tyranny of the Rocket Equation ---
https://adventofcode.com/2019/day/1
"""
from aocd import data
import numpy as np


A = np.fromstring(data, dtype=int, sep="\n")
total = 0
while A.any():
    A = (A // 3 - 2).clip(0)
    if not total:
        print("part a:", A.sum())
    total += A.sum()
print("part b:", total)
