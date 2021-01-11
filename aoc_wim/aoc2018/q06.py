"""
--- Day 6: Chronal Coordinates ---
https://adventofcode.com/2018/day/6
"""
from io import StringIO
import numpy as np
from aocd import data


vs = np.loadtxt(StringIO(data), dtype=int, delimiter=",")
w, h = vs.max(axis=0) + 1
n = len(vs)
d_max = 32 if n == 6 else 10000
ps = np.mgrid[:w, :h].transpose(1, 2, 0).reshape(-1, 1, 2)
ds = np.abs(ps - vs).sum(axis=2)
d = ds.argmin(axis=1)
ties = d != n - 1 - np.fliplr(ds).argmin(axis=1)
d[ties] = -1
border = {*d[:w], *d[-w:], *d[::h], *d[::-h]}
areas = [(d == c).sum() for c in range(n) if c not in border]
print("part a:", max(areas))
print("part b:", (ds.sum(axis=1) < d_max).sum())
