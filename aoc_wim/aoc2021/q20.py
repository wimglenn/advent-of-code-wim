"""
--- Day 20: Trench Map ---
https://adventofcode.com/2021/day/20
"""
from aocd import data
import numpy as np
from scipy.signal import convolve2d

s, grid = data.split("\n\n")
s = np.array([c == "#" for c in s])
im = np.array([[*r] for r in grid.splitlines()]) == "#"
kernel = 2 ** np.arange(9).reshape(3, 3)
for i in range(50):
    im = s[convolve2d(im, kernel, fillvalue=s[0]*i % 2)]
    if i == 1:
        print("part a:", im.sum())
print("part b:", im.sum())
