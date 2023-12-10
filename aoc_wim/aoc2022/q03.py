"""
--- Day 3: Rucksack Reorganization ---
https://adventofcode.com/2022/day/3
"""
from itertools import batched

from aocd import data

a = 0
for line in data.splitlines():
    i = len(line) // 2  # midpoint
    left, right = line[:i], line[i:]
    [c] = set(left).intersection(right)
    a += c.isupper() * 26
    a += ord(c.lower()) - ord("a") + 1

b = 0
for s1, s2, s3 in batched(data.splitlines(), 3):
    [c] = set(s1).intersection(s2, s3)
    b += c.isupper() * 26
    b += ord(c.lower()) - ord("a") + 1

print("answer_a:", a)
print("answer_b:", b)
