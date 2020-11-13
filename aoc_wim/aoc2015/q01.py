"""
--- Day 1: Not Quite Lisp ---
https://adventofcode.com/2015/day/1
"""
from aocd import data


direction = {"(": +1, ")": -1}
basement = None
floor = 0
for i, c in enumerate(data, 1):
    floor += direction[c]
    if basement is None and floor == -1:
        basement = i


print("part a:", floor)
print("part b:", basement)
