import numpy as np
from aocd import data


def part_a(data):
    A = np.zeros(1000000, dtype=int)
    for i in range(1, 1000000):
        A[i::i] += i * 10
    return np.argmax(A > int(data))


def part_b(data):
    A = np.zeros(1000000, dtype=int)
    for i in range(1, 1000000):
        A[i::i][:50] += i * 11
    return np.argmax(A > int(data))


print("part a:", part_a(data))
print("part b:", part_b(data))
