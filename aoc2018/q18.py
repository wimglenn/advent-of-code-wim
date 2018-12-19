from aocd import data
import numpy as np
from scipy.signal import convolve2d
import time


test_data = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""


def parsed(data):
    h = len(data.splitlines())
    A = np.fromiter(data.replace('\n', ''), dtype='<U1').reshape(h, -1)
    A = (A=="|").astype(complex) + (A=="#").astype(complex)*1j
    return A


def dump(A, dt=0.1):
    # d = {0: ".", 1: "|", 1j: "#"}
    d = {0: "  ", 1: "🌲", 1j: " ⛏"}
    print("\33c")
    for row in A:
        print(*[d[c] for c in row], sep='')
    print()
    time.sleep(dt)


def mutate(A0):
    k = np.ones((3, 3), dtype=complex)
    B = convolve2d(A0, k, mode='same')
    A1 = A0.copy()
    A1[(A0==0) & (B.real>=3)] = 1
    A1[(A0==1) & (B.imag>=3)] = 1j
    A1[(A0==1j) & ((B.imag < 2) | (B.real==0))] = 0
    return A1


def run(data, minutes=10, debug=False):
    A = parsed(data)
    m = minutes
    seen = {A.tostring(): m}
    while m > 0:
        m -= 1
        A = mutate(A)
        if debug:
            dump(A)
        s = A.tostring()
        if s in seen:
            delta = seen[s] - m
            m %= delta
        seen[s] = m
    return (A==1).sum() * (A==1j).sum()


debug = True
assert run(test_data, minutes=10, debug=debug) == 1147

a = run(data, minutes=10, debug=debug)
print(a)  # 603098

b = run(data, minutes=1000000000, debug=debug)
print(b)  # 210000
