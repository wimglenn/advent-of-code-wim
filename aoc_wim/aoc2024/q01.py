"""
--- Day 1: Historian Hysteria ---
https://adventofcode.com/2024/day/1
"""
from aocd import data
from collections import Counter

ns = [int(n) for n in data.split()]
xs = sorted(ns[0::2])
ys = sorted(ns[1::2])
a = sum(abs(x - y) for x, y in zip(xs, ys))
rcount = Counter(ys)
b = sum(x * rcount[x] for x in xs)
print("answer_a:", a)
print("answer_b:", b)
