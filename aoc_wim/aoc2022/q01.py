"""
--- Day 1: Calorie Counting ---
https://adventofcode.com/2022/day/1
"""
from heapq import nlargest

from aocd import data

cals = []
for chunk in data.split("\n\n"):
    cals.append(sum(map(int, chunk.split())))

print("answer_a:", max(cals))
print("answer_b:", sum(nlargest(3, cals)))
