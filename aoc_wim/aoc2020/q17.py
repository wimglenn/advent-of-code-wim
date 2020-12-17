"""
--- Day 17: Conway Cubes ---
https://adventofcode.com/2020/day/17
"""
from aocd import data
import numpy as np
from scipy.signal import convolve


def evolve(A, n=6):
    kernel = np.ones((3,) * A.ndim, dtype=A.dtype)
    kernel[(1,) * A.ndim] = 0  # hollow center
    for _ in range(n):
        C = convolve(A, kernel)
        A = np.pad(A, pad_width=1)
        A = ((A == 1) & ((C == 2) | (C == 3))) | ((A == 0) & (C == 3))
        A = A.astype(int)
    return A


A0 = (np.array([[*r] for r in data.splitlines()]) == "#").astype(int)
print("part a:", evolve(A0[..., None]).sum())
print("part b:", evolve(A0[..., None, None]).sum())
