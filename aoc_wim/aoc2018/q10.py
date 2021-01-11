"""
--- Day 10: The Stars Align ---
https://adventofcode.com/2018/day/10
"""
import re
import numpy as np
from aocd import data
from aoc_wim.ocr import AOCR
from aoc_wim.zgrid import ZGrid


def varianceish(a):
    return a.std(axis=1)[:2].sum()


numbers = re.findall(r"-?\d+", data)
a = np.array(numbers).astype(int).reshape(-1, 4).T
t = 0
minv = varianceish(a)
while True:
    a[:2] += a[2:]
    v = varianceish(a)
    minv = min(v, minv)
    if v > minv:
        ps = a[:2] - a[2:]  # back up one step
        g = ZGrid({complex(*p): 1 for p in ps.T})
        print("part a:", AOCR[g])
        print("part b:", t)
        break
    t += 1
