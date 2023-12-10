"""
--- Day 20: Trench Map ---
https://adventofcode.com/2021/day/20
"""
import numpy as np
from aocd import data
from scipy.signal import convolve2d

s, grid = data.split("\n\n")
s = np.array([c == "#" for c in s.replace("\n", "")])
im = np.array([[*r] for r in grid.splitlines()]) == "#"
kernel = 2 ** np.arange(9).reshape(3, 3)
for i in range(50):
    im = s[convolve2d(im, kernel, fillvalue=s[0]*i % 2)]
    if i == 1:
        print("answer_a:", im.sum())
print("answer_b:", im.sum())
