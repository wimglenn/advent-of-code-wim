"""
--- Day 18: Like a GIF For Your Yard ---
https://adventofcode.com/2015/day/18
"""
import numpy as np
from aocd import data
from scipy.signal import convolve2d


kernel = np.ones((3, 3), dtype=int)
kernel[1, 1] = 0


def evolve(A, part="a"):
    """conway's game of life"""
    C = convolve2d(A, kernel, mode="same")
    A = ((A == 1) & ((C == 2) | (C == 3))) | ((A == 0) & (C == 3))
    return A.astype(int)


def animate(data, part="a"):
    A = np.array([[c == "#" for c in r] for r in data.splitlines()]).astype(int)
    if part == "b":
        A[0, 0] = A[0, -1] = A[-1, 0] = A[-1, -1] = 1
    iterations = 1 if A.shape == (6, 6) else 100
    for i in range(iterations):
        A = evolve(A, part)
        if part == "b":
            A[0, 0] = A[0, -1] = A[-1, 0] = A[-1, -1] = 1
    return A.sum()


print("answer_a:", animate(data, part="a"))
print("answer_b:", animate(data, part="b"))
