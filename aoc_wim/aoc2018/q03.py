"""
--- Day 3: No Matter How You Slice It ---
https://adventofcode.com/2018/day/3
"""
from types import SimpleNamespace

import numpy as np
from aocd import data
from parse import parse


template = "#{id:d} @ {col:d},{row:d}: {w:d}x{h:d}"
claims = [SimpleNamespace(**parse(template, s).named) for s in data.splitlines()]
W = max(c.col + c.w for c in claims)
H = max(c.row + c.h for c in claims)
A = np.zeros((H, W, len(claims)), dtype=int)

for c in claims:
    A[c.row : c.row + c.h, c.col : c.col + c.w, c.id - 1] = 1
print("part a:", (A.sum(axis=2) > 1).sum())

for c in claims:
    if A[c.row : c.row + c.h, c.col : c.col + c.w, :].sum() == c.w * c.h:
        print("part b:", c.id)
        break
