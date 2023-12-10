"""
--- Day 8: Two-Factor Authentication ---
https://adventofcode.com/2016/day/8
"""
import numpy as np
from aocd import data

from aoc_wim.ocr import AOCR


def animate(A, line):
    if line.startswith("rect"):
        w, h = [int(x) for x in line.split()[1].split("x")]
        A[0:h, 0:w] = "#"
    elif line.startswith("rotate"):
        i, shift = [int(x) for x in line.split("=")[1].split(" by ")]
        item = (i, slice(None)) if "row" in line else (slice(None), i)
        A[item] = np.roll(A[item], shift)
    return A


lines = data.splitlines()
im = (3, 7) if len(lines) == 4 else (6, 50)
A = np.full(im, ".")
for line in lines:
    A = animate(A, line)
print("answer_a:", (A == "#").sum())
print("answer_b:", AOCR[A])
