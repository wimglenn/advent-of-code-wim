"""
--- Day 15: Dueling Generators ---
https://adventofcode.com/2017/day/15
"""
import numpy as np
from aocd import data
from parse import parse

template = (
    "Generator A starts with {:d}\n"
    "Generator B starts with {:d}"
)
a0, b0 = parse(template, data).fixed
fa = 16807
fb = 48271
d = 0x7fffffff

AB = np.array([[a0, b0]], dtype=np.int64) * (fa, fb) % d
while len(AB) < 40_000_000:
    f = pow(fa, len(AB), d), pow(fb, len(AB), d)
    AB = np.vstack([AB, AB * f % d])

AB &= 0xffff
A, B = AB.T
A4 = A[A & 0b11 == 0]
B8 = B[B & 0b111 == 0]
print("part a:", (A[:40_000_000] == B[:40_000_000]).sum())
print("part b:", (A4[:5_000_000] == B8[:5_000_000]).sum())
