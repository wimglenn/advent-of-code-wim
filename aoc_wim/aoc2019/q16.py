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
    X = np.hstack([x] * (-pos_r // w + 1))
    X = X[pos_r:]
    for _ in range(n):
        X = X[::-1].cumsum()[::-1] % 10
    return ''.join(str(n) for n in list(X)[pos_r:pos_r+8])


assert part_a("12345678", 1) == "48226158"
assert part_a("12345678", 2) == "34040438"
assert part_a("12345678", 3) == "03415518"
assert part_a("12345678", 4) == "01029498"


tests_a = """\
80871224585914546619083218645595 becomes 24176176
19617804207202209144916044189917 becomes 73745418
69317163492948606335995924319873 becomes 52432133
"""
for test in tests_a.splitlines():
    test_data, sep, expected = test.partition(" becomes ")
    assert part_a(test_data) == expected


tests_b = """\
03036732577212944063491565474664 becomes 84462026
02935109699940807407585447034323 becomes 78725270
03081770884921959731165446850517 becomes 53553731
"""
for test in tests_b.splitlines():
    test_data, sep, expected = test.partition(" becomes ")
    assert part_b(test_data) == expected


print(part_a(data))
print(part_b(data))
