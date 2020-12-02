"""
--- Day 18: Like a GIF For Your Yard ---
https://adventofcode.com/2015/day/18
"""
import numpy as np
from aocd import data
from scipy.signal import convolve2d
from aoc_wim.zgrid import ZGrid


def parsed(data, part="a"):
    grid = ZGrid(data)
    A = (np.array(grid) == "#").astype(int)
    if part == "b":
        A[0, 0] = A[0, -1] = A[-1, 0] = A[-1, -1] = 1
    return A


kernel = np.ones((3, 3), dtype=int)
kernel[1, 1] = 0


def evolve(A, part="a"):
    """conway's game of life"""
    C = convolve2d(A, kernel, mode="same")
    A = ((A == 1) & ((C == 2) | (C == 3))) | ((A == 0) & (C == 3))
    A = A.astype(int)
    if part == "b":
        A[0, 0] = A[0, -1] = A[-1, 0] = A[-1, -1] = 1
    return A


def animate(data, iterations=100, part="a"):
    A = parsed(data, part)
    for i in range(iterations):
        A = evolve(A, part)
    return A.sum()


if __name__ == "__main__":
    print(animate(data, part="a"))
    print(animate(data, part="b"))
