from aocd import data
from aoc2017.q10 import knot_hash
import numpy as np
from scipy.ndimage.measurements import label

def f(data):
    s = ''.join(f"{int(knot_hash(f'{data}-{i}'), 16):0128b}" for i in range(128))
    return s.count('1'), label(np.fromiter(s, dtype=int).reshape(128, 128))[1]

assert f('flqrgnkx') == (8108, 1242)

a, b = f(data)
print("part a:", a)
print("part b:", b)
