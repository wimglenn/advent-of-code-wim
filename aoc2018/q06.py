from aocd import data
from io import StringIO
import numpy as np


test_data = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""


def part_ab(data, d_max=10000):
    vs = np.loadtxt(StringIO(data), dtype=int, delimiter=',')
    shape = vs.max(axis=0) + 1
    A = np.zeros(shape, dtype=int) - 1
    B = np.zeros(shape, dtype=bool)
    py, px = np.mgrid[:shape[0],:shape[1]]
    ps = np.c_[py.ravel(), px.ravel()]
    for p in ps:
        distances = np.abs(vs - p).sum(axis=1)
        min_d = distances.min()
        if (distances == min_d).sum() == 1:
            A[tuple(p)] = np.argmin(distances)
        if distances.sum() < d_max:
            B[tuple(p)] = True
    borders = {*A[0], *A[-1], *A.T[0], *A.T[-1]}
    choices = set(range(len(vs))) - borders
    areas = [(A==c).sum() for c in choices]
    a = max(areas)
    b = B.sum()
    return a, b


assert part_ab(test_data, d_max=32) == (17, 16)
a, b = part_ab(data)
print(a)  # 3293
print(b)  # 45176
