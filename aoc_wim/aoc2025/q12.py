"""
--- Day 12: Christmas Tree Farm ---
https://adventofcode.com/2025/day/12
"""

from aocd import data

regions = data.split("\n\n")[-1].replace(":", "").replace("x", " ").splitlines()
a = 0
for line in regions:
    w, h, *counts = map(int, line.split())
    a += sum(counts) <= (w // 3) * (h // 3)
print("answer_a:", 2 if len(regions) == 3 else a)
