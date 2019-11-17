import numpy as np
from aocd import data
from scipy.signal import convolve2d


test_data = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""


def animate(data, iterations=100, corners_on=False):
    A = np.vstack(
        [
            np.array([{".": 0, "#": 1}[x] for x in row], dtype=int)
            for row in data.splitlines()
        ]
    )
    if corners_on:
        A[0, 0] = A[0, -1] = A[-1, 0] = A[-1, -1] = 1
    kernel = np.ones((3, 3), dtype=int)
    kernel[1, 1] = 0
    for i in range(iterations):
        C = convolve2d(A, kernel, mode="same")
        A = ((A == 1) & ((C == 2) | (C == 3))) | ((A == 0) & (C == 3))
        A = A.astype(int)
        if corners_on:
            A[0, 0] = A[0, -1] = A[-1, 0] = A[-1, -1] = 1
    return A.sum()


assert animate(test_data, iterations=4) == 4
assert animate(test_data, iterations=5, corners_on=True) == 17

print(animate(data))
print(animate(data, corners_on=True))
