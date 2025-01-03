"""
--- Day 25: Code Chronicle ---
https://adventofcode.com/2024/day/25
"""
from aocd import data

from aoc_wim.zgrid import ZGrid


chunks = data.split("\n\n")
keys = []
locks = []
for chunk in chunks:
    zs = set(ZGrid(chunk).z("#", first=False))
    L = keys if chunk[0] == "." else locks
    L.append(zs)

a = sum(1 for lock in locks for key in keys if not lock & key)
print("answer_a:", a)
