from aocd import data
from q10 import knot_hash
import numpy as np
from skimage.morphology import label

def f(data):
    s = ''.join(format(int(knot_hash(f'{data}-{i}'), 16), '0128b') for i in range(128))
    a = np.fromiter(s, dtype=int).reshape(128, 128)
    return a.sum(), label(a, connectivity=1, return_num=True)[1]

assert f('flqrgnkx') == (8108, 1242)

a, b = f(data)
print(a)  # part a: 8222
print(b)  # part b: 1086
