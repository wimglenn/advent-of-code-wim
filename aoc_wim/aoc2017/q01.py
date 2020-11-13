"""
--- Day 1: Inverse Captcha ---
https://adventofcode.com/2017/day/1
"""
import numpy as np
from aocd import data


def part_a(data, roll=1):
    a = np.fromiter(data, dtype=int)
    b = np.roll(a, roll)
    return a[a == b].sum()


def part_b(data):
    return part_a(data, roll=len(data) // 2)


print("part a:", part_a(data))
print("part b:", part_b(data))
