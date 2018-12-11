from aocd import data
import numpy as np
from scipy.signal import convolve2d


def gen_grid(data):
    d = int(data)
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


def gpl(data, x, y):
    g = gen_grid(data)
    return g[y - 1, x - 1]


assert gpl(8, 3, 5) == 4
assert gpl(57, 122, 79) == -5
assert gpl(39, 217, 196) == 0
assert gpl(71, 101, 153) == 4


mygrid = gen_grid(data)


def max_power(grid=mygrid, kernels=(3,)):
    maxs = []
    for k in kernels:
        kernel = np.ones((k, k), dtype=int)
        c = convolve2d(grid, kernel, mode="valid")
        y, x = np.unravel_index(c.argmax(), c.shape)
        maxs.append((c[y, x], x + 1, y + 1, k))
    return max(maxs)


def part_a(grid=mygrid):
    m, x, y, k = max_power(grid)
    return f"{x},{y}"


def part_b(grid=mygrid, search_limit=20):
    m, x, y, k = max_power(grid, kernels=range(1, search_limit))
    return f"{x},{y},{k}"


grid18 = gen_grid(18)
grid42 = gen_grid(42)
assert max_power(grid18) == (29, 33, 45, 3)
assert max_power(grid42) == (30, 21, 61, 3)
assert part_b(grid18) == "90,269,16"
assert part_b(grid42) == "232,251,12"


a = part_a()
print(a)  # part a: 20,46

b = part_b()
print(b)  # part b: 231,65,14
