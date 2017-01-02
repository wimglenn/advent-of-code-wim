from aocd import data
import numpy as np


def part_a(data):
    A = np.zeros(1000000, dtype=int)
    for i in range(1,1000000):
        A[i::i] += i*10
    return np.argmax(A>int(data))


def part_b(data):
    A = np.zeros(1000000, dtype=int)
    for i in range(1,1000000):
        A[i::i][:50] += i*11
    return np.argmax(A>int(data))


print(part_a(data))  # 831600
print(part_b(data))  # 884520
