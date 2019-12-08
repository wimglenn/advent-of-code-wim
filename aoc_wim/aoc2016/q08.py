import numpy as np
from aocd import data
from aoc_wim.ocr import AOCR


def parsed(data):
    W, H = 50, 6
    A = np.zeros((H, W), dtype=bool)
    for line in data.splitlines():
        if line.startswith("rect"):
            w, h = [int(x) for x in line.split()[1].split("x")]
            A[0:h, 0:w] = True
        elif line.startswith("rotate"):
            i, shift = [int(x) for x in line.split("=")[1].split(" by ")]
            item = (i, slice(None)) if "row" in line else (slice(None), i)
            A[item] = np.roll(A[item], shift)
    return A


def part_a(data):
    A = parsed(data)
    return A.sum()


def part_b(data):
    A = parsed(data)
    return AOCR[A]


print("part a:", part_a(data))
print("part b:", part_b(data))
