"""
--- Day 8: Space Image Format ---
https://adventofcode.com/2019/day/8
"""
from aocd import data
import numpy as np
from aoc_wim.ocr import AOCR

rows, cols = 6, 25
a = np.fromiter(data, int).reshape((-1, rows, cols))
layer = min(a, key=lambda v: (v == 0).sum())
print((layer == 1).sum() * (layer == 2).sum())

img = np.ones_like(layer) * 2
for layer in a:
    np.copyto(img, layer, where=(img == 2))

txt = AOCR[img]
print(txt)
