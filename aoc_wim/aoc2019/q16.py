"""
--- Day 16: Flawed Frequency Transmission ---
https://adventofcode.com/2019/day/16
"""
from aocd import data
from itertools import cycle
import numpy as np


def square_wave(w=1):
    base = [0] * w + [1] * w + [0] * w + [-1] * w
    gen = cycle(base)
    next(gen)
    return gen


def part_a(data, n=100):
    x = np.fromiter(data, int)
    [w] = x.shape
    waves = [square_wave(i + 1) for i in range(w)]
    A = np.array([[next(g) for _ in range(w)] for g in waves], dtype=int)
    for _ in range(n):
        x = abs((A * x).sum(axis=1)) % 10
    result = ''.join(str(n) for n in x[:8])
    return result


def part_b(data, n=100):
    x = np.fromiter(data, int)
    [w] = x.shape
    pos = int(data[:7])
    pos_r = pos - w * 10_000
    stack = -pos_r // w + 1
    if stack <= 0:
        return
    X = np.hstack([x] * stack)
    X = X[pos_r:]
    for _ in range(n):
        X = X[::-1].cumsum()[::-1] % 10
    return ''.join(str(n) for n in list(X)[pos_r:pos_r+8])


if __name__ == "__main__":
    print(part_a(data))
    print(part_b(data))
