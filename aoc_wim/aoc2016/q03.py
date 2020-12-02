"""
--- Day 3: Squares With Three Sides ---
https://adventofcode.com/2016/day/3
"""
import numpy as np
from aocd import data


A = np.fromstring(data, sep=" ", dtype=int)
R = A.reshape(-1, 3).T
C = R.reshape(-1, 3).T

for A in R, C:
    T = A[0] + A[1] > A[2]
    T &= A[0] + A[2] > A[1]
    T &= A[1] + A[2] > A[0]
    print(T.sum())
