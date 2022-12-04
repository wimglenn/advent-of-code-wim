"""
--- Day 4: Camp Cleanup ---
https://adventofcode.com/2022/day/4
"""
from aocd import data
from parse import parse

a = b = 0
for line in data.splitlines():
    l1, r1, l2, r2 = parse("{:d}-{:d},{:d}-{:d}", line).fixed
    if l1 > l2 or (l1 == l2 and r1 < r2):
        l1, r1, l2, r2 = l2, r2, l1, r1
    a += r2 <= r1
    b += r1 >= l2

print("part a:", a)
print("part b:", b)
