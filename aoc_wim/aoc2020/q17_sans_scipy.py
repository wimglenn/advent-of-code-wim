"""
--- Day 17: Conway Cubes ---
https://adventofcode.com/2020/day/17
"""
from aocd import data
from itertools import product
import numpy as np


def evolve(A):
    A0 = np.pad(A, pad_width=1)
    A1 = A0.copy()
    for pos in [*product(*[range(d) for d in A0.shape])]:
        slices = [slice(max(x-1, 0), x+2) for x in pos]
        n_on = A0[tuple(slices)].sum()
        if A0[pos] and not 3 <= n_on <= 4:
            A1[pos] = 0
        if not A0[pos] and n_on == 3:
            A1[pos] = 1
    return A1


A0 = np.array([[v == "#" for v in line] for line in data.splitlines()], dtype=int)
for dimension, part in enumerate("ab", start=3):
    A = A0.copy()[(...,) + (None,) * (dimension - A0.ndim)]
    for _ in range(6):
        A = evolve(A)
    print("part", part, A.sum())
