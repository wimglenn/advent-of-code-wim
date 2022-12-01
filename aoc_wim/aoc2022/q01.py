"""
--- Day 1: Calorie Counting ---
https://adventofcode.com/2022/day/1
"""
from aocd import data
from heapq import nlargest

cals = []
for chunk in data.split("\n\n"):
    cals.append(sum(map(int, chunk.split())))

print("part a:", max(cals))
print("part b:", sum(nlargest(3, cals)))
