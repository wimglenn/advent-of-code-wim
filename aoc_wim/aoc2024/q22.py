"""
--- Day 22: Monkey Market ---
https://adventofcode.com/2024/day/22
"""
from aocd import data
from collections import Counter
import numpy as np


n = np.array([*map(int, data.split())])
N = np.empty((2001, len(n)), dtype=int)
N[0] = n
for i in range(1, 2001):
    n ^= (n << 6) & 0xffffff
    n ^= (n >> 5)
    n ^= (n << 11) & 0xffffff
    N[i] = n
print("answer_a:", n.sum())

N %= 10
dN = N[1:] - N[:-1]
dN3 = dN[0:-3] << 15
dN2 = dN[1:-2] << 10
dN1 = dN[2:-1] << 5
key = dN[3:] + dN3 + dN2 + dN1

bananas = Counter()
for i in range(len(n)):
    seq = key.T[i][::-1].tolist()
    price = N[4:].T[i][::-1].tolist()
    bananas += dict(zip(seq, price))
print("answer_b:", max(bananas.values()))
