"""
--- Day 9: Mirage Maintenance ---
https://adventofcode.com/2023/day/9
"""
import numpy as np
from aocd import data


n = len(data.splitlines())
A = A0 = np.fromstring(data, sep=" ", dtype=int).reshape(n, -1).T
As = [A0]
while A.any():
    A = A[1:] - A[:-1]
    As.append(A)

As.reverse()
Ba = Bb = np.pad(A, [(0, 1), (0, 0)])
for A0, A1 in zip(As, As[1:]):
    Ba = np.vstack([A0[:1], A1 + Ba])
    Bb = np.vstack([A1 - Bb, A0[-1:]])

print("answer_a:", int(Ba[-1].sum()))
print("answer_b:", int(Bb[0].sum()))
