"""
--- Day 20: Infinite Elves and Infinite Houses ---
https://adventofcode.com/2015/day/20
"""
import numpy as np
from aocd import data


A = np.zeros(1000000, dtype=int)
B = A.copy()
for i in range(1, 1000000):
    A[i::i] += i * 10
    B[i::i][:50] += i * 11


assert A[1:10].tolist() == [10, 30, 40, 70, 60, 120, 80, 150, 130]
print("part a:", np.argmax(A > int(data)))
print("part b:", np.argmax(B > int(data)))
