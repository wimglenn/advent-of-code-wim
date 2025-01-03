"""
--- Day 18: Like a GIF For Your Yard ---
https://adventofcode.com/2015/day/18
"""
import numpy as np
from aocd import data
from aocd import extra
from scipy.signal import convolve2d

from aoc_wim.zgrid import ZGrid


kernel = np.ones((3, 3), dtype=int)
kernel[1, 1] = 0


def evolve(A):
    """conway's game of life"""
    C = convolve2d(A, kernel, mode="same")
    A = ((A == 1) & ((C == 2) | (C == 3))) | ((A == 0) & (C == 3))
    return A.astype(int)


def animate(data, part="a"):
    grid = ZGrid(data, transform={"#": 1, ".": 0})
    A = np.array(grid)
    if part == "b":
        A[0, 0] = A[0, -1] = A[-1, 0] = A[-1, -1] = 1
    for i in range(extra.get("iterations", 100)):
        A = evolve(A)
        if part == "b":
            A[0, 0] = A[0, -1] = A[-1, 0] = A[-1, -1] = 1
    return A.sum()


print("answer_a:", animate(data, part="a"))
print("answer_b:", animate(data, part="b"))
