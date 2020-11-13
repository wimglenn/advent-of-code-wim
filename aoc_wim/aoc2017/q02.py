"""
--- Day 2: Corruption Checksum ---
https://adventofcode.com/2017/day/2
"""
from itertools import combinations

from aocd import data


checksum = result = 0
for line in data.splitlines():
    row = [int(x) for x in line.split()]
    checksum += max(row) - min(row)
    for x, y in combinations(row, 2):
        denominator, numerator = sorted([x, y])
        quotient, remainder = divmod(numerator, denominator)
        if not remainder:
            result += quotient
            break

print("part a:", checksum)
print("part b:", result)
