"""
--- Day 6: Custom Customs ---
https://adventofcode.com/2020/day/6
"""
from aocd import data

a = b = 0
for block in data.split("\n\n"):
    s = {*block} - {"\n"}
    a += len(s)
    b += len(s.intersection(*block.splitlines()))

print(a)
print(b)
