"""
--- Day 18: Settlers of The North Pole ---
https://adventofcode.com/2018/day/18
"""
import time
import numpy as np
from aocd import data
from scipy.signal import convolve2d


def parsed(data):
    h = len(data.splitlines())
    A = np.fromiter(data.replace("\n", ""), dtype="<U1").reshape(h, -1)
    A = (A == "|").astype(complex) + (A == "#").astype(complex) * 1j
    return A


def draw(A, dt=0.1):
    # d = {0: ".", 1: "|", 1j: "#"}
    d = {0: "  ", 1: "🌲", 1j: " ⛏"}
    print("\33c")
    for row in A:
        print(*[d[c] for c in row], sep="")
    print()
    time.sleep(dt)


def mutate(A0):
    k = np.ones((3, 3), dtype=complex)
    B = convolve2d(A0, k, mode="same")
    A1 = A0.copy()
    A1[(A0 == 0) & (B.real >= 3)] = 1
    A1[(A0 == 1) & (B.imag >= 3)] = 1j
    A1[(A0 == 1j) & ((B.imag < 2) | (B.real == 0))] = 0
    return A1


def evolve(data, minutes=10):
    A = parsed(data)
    m = minutes
    seen = {A.tobytes(): m}
    while m > 0:
        m -= 1
        A = mutate(A)
        # draw(A)
        s = A.tobytes()
        if s in seen:
            delta = seen[s] - m
            m %= delta
        seen[s] = m
    return (A == 1).sum() * (A == 1j).sum()


print("part a:", evolve(data, minutes=10))
print("part b:", evolve(data, minutes=1000000000))
