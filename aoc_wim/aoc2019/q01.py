from aocd import data

import numpy as np


def fuel(data, part="a"):
    A = np.fromstring(data, dtype=int, sep="\n")
    total = 0
    while A.any():
        A = (A // 3 - 2).clip(0)
        total += A.sum()
        if part == "a":
            break
    return total


test_data = """
12
14
1969
100756
"""

assert fuel(test_data, part="a") == sum([2, 2, 654, 33583])
assert fuel(test_data, part="b") == sum([2, 2, 966, 50346])

print(fuel(data, part="a"))
print(fuel(data, part="b"))
