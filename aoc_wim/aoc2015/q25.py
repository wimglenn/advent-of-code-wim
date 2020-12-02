"""
--- Day 25: Let It Snow ---
https://adventofcode.com/2015/day/25
"""
from aocd import data


words = data.split()
row = int(words[-3].rstrip(","))
col = int(words[-1].rstrip("."))


def n(row, col):
    i = (row + col) * (row + col) + 2 - col - 3 * row
    return i // 2


m = 252533
d = 33554393
i = n(row, col)
code = 20151125
for _ in range(1, i):
    code = m * code % d

print(code)
