"""
--- Day 8: Space Image Format ---
https://adventofcode.com/2019/day/8
"""
import numpy as np
from aocd import data
from aocd import extra

from aoc_wim.ocr import AOCR

w = extra.get("image_width", 25)
h = extra.get("image_height", 6)
a = np.fromiter(data, int).reshape((-1, h, w))
layer = min(a, key=lambda v: (v == 0).sum())
print("answer_a:", (layer == 1).sum() * (layer == 2).sum())

img = np.ones_like(layer) * 2
for layer in a:
    np.copyto(img, layer, where=(img == 2))

if w != 3:
    print("answer_b:", AOCR[img])
