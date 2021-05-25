"""
--- Day 15: Dueling Generators ---
https://adventofcode.com/2017/day/15
"""
import numpy as np
from aocd import data
from parse import parse

template = "Generator A starts with {:d}\nGenerator B starts with {:d}"
a0, b0 = parse(template, data).fixed
fa = 16807
fb = 48271
d = 0x7fffffff

f = np.array([[fa, fb]], dtype=np.uint)
A = np.array([[a0, b0]], dtype=np.uint) * f % d
while A.shape[0] < 40_000_000:
    f = np.array([[pow(fa, A.shape[0], d), pow(fb, A.shape[0], d)]], dtype=np.uint)
    A = np.vstack([A, A * f % d])

A &= 0xffff
A4 = A[:, 0][A[:, 0] & 0b11 == 0][:5_000_000]
B8 = A[:, 1][A[:, 1] & 0b111 == 0][:5_000_000]
print("part a:", (A[:40_000_000][:, 0] == A[:40_000_000][:, 1]).sum())
print("part b:", (A4 == B8).sum())
