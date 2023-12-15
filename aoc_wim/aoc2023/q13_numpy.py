"""
--- Day 13: Point of Incidence ---
https://adventofcode.com/2023/day/13
"""
import numpy as np
from aocd import data

a = b = 0
for chunk in data.split("\n\n"):
    h = chunk.count("\n") + 1
    A = np.fromiter(chunk.replace("\n", ""), dtype="<U1").reshape(h, -1)
    for A, f in zip([A, A.T], [100, 1]):
        h = len(A)
        for i in range(1, h):
            A1 = A[max(2*i-h,0):i]
            A2 = A[i:i+min(i,h-i)][::-1]
            match (A1 != A2).sum():
                case 0: a += f * i
                case 1: b += f * i

print("answer_a:", a)
print("answer_b:", b)
