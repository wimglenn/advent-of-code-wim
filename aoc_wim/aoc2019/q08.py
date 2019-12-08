from aocd import data
import numpy as np
from aoc_wim.ocr import AOCR

rows, cols = 6, 25
a = np.fromiter(data, int).reshape((-1, rows, cols))
layer = min(a, key=lambda v: (v == 0).sum())
print((layer == 1).sum() * (layer == 2).sum())

letters = [""] * (cols // 5)
for row in range(rows):
    for col in range(cols):
        i, rem = divmod(col, 5)
        prefix = "\n" * (row > 0 and rem == 0)
        for z in a[:, row, col]:
            char = ".# "[z]
            if char != " ":
                letters[i] += prefix + char
                break

for letter in letters:
    print(AOCR[letter], end="")
print()
