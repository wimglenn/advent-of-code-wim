"""
--- Day 6: Tuning Trouble ---
https://adventofcode.com/2022/day/6
"""
from aocd import data
from collections import Counter


def marker(data, n):
    counts = Counter(data[:n])
    i = n
    while len(counts) < n:
        if data[i] != data[i - n]:
            counts += {data[i]: 1, data[i - n]: -1}
        i += 1
    return i


print("part a:", marker(data, 4))
print("part b:", marker(data, 14))
