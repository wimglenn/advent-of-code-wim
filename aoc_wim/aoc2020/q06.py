"""
--- Day 6: Custom Customs ---
https://adventofcode.com/2020/day/6
"""
from aocd import data

a = 0
b = 0
for block in data.split("\n\n"):
    s = set(block) - {"\n"}
    a += len(s)
    b += len(s.intersection(*map(set, block.splitlines())))

print(a)
print(b)
