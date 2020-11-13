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


A = np.full((6, 50), ".")
for line in data.splitlines():
    A = animate(A, line)


if __name__ == "__main__":
    print("part a:", (A == "#").sum())
    print("part b:", AOCR[A])
