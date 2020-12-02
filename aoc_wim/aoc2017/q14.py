"""
--- Day 14: Disk Defragmentation ---
https://adventofcode.com/2017/day/14
"""
import numpy as np
from aocd import data
from scipy.ndimage.measurements import label

from aoc_wim.aoc2017.q10 import knot_hash

s = "".join(f"{int(knot_hash(f'{data}-{i}'), 16):0128b}" for i in range(128))
print("part a:", s.count("1"))
print("part b:", label(np.fromiter(s, dtype=int).reshape(128, 128))[1])
