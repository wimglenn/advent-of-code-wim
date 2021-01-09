"""
--- Day 24: Lobby Layout ---
https://adventofcode.com/2020/day/24
"""
from aocd import data
import re
from aoc_wim import zgrid
import numpy as np
from scipy.signal import convolve2d


pat = r"(se|sw|ne|nw|e|w)"
grid = zgrid.ZGrid(on=1, off=0)
for i, line in enumerate(data.splitlines()):
    steps = re.findall(pat, line)
    z = sum([zgrid.hexH[s] for s in steps])
    grid[z] = 1 - grid.get(z, 0)
    # grid.draw_hex(glyph=0, orientation="H", clear=True, title=f" flip {i} ")
print("part a:", grid.count(1))

# conway's game of life on a hexgrid
A = np.array(grid)
kernel = 1 - np.flipud(np.eye(3, dtype=int))
for day in range(1, 101):
    A = np.pad(A, pad_width=1)
    C = convolve2d(A, kernel, mode="same")
    A = ((A == 1) & ((C == 1) | (C == 2))) | ((A == 0) & (C == 2))
    A = A.astype(int)
    if day <= 10 or day % 10 == 0:
        print(f"Day {day}:", A.sum())
    if day == 10:
        print()
print("part b:", A.sum())
