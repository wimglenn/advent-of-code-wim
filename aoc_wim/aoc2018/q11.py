"""
--- Day 11: Chronal Charge ---
https://adventofcode.com/2018/day/11
"""
import numpy as np
from aocd import data
from scipy.signal import convolve2d


def gen_grid(data):
    d = int(data or 0)
    n = 300
    a = np.empty((n, n), dtype=int)
    v = np.arange(0, n, dtype=int) + 1
    a[:] = v + 10
    a[:] *= v.reshape(-1, 1)
    a += d
    a[:] *= v + 10
    a %= 1000
    a //= 100
    a -= 5
    return a


def max_power(grid, kernels=(3,)):
    maxs = []
    for k in kernels:
        kernel = np.ones((k, k), dtype=int)
        c = convolve2d(grid, kernel, mode="valid")
        y, x = np.unravel_index(c.argmax(), c.shape)
        maxs.append((c[y, x], x + 1, y + 1, k))
    return max(maxs)


grid = gen_grid(data)

_, x, y, _ = max_power(grid)
print("part a:", f"{x},{y}")

_, x, y, k = max_power(grid, kernels=range(1, 20))
print("part b:", f"{x},{y},{k}")
