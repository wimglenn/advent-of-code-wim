"""
--- Day 6: Tuning Trouble ---
https://adventofcode.com/2022/day/6
"""
from aocd import data
from collections import deque


def marker(data, s):
    d = deque(maxlen=s)
    for i, c in enumerate(data, 1):
        d.append(c)
        if len(set(d)) == s:
            return i


print("part a:", marker(data, 4))
print("part b:", marker(data, 14))
