"""
--- Day 9: Encoding Error ---
https://adventofcode.com/2020/day/9
"""
from aocd import data
from wimpy import chunks
from collections import Counter
from aoc_wim.aoc2020 import find_pair

numbers = [int(x) for x in data.splitlines()]
n = 25
if len(numbers) < n:
    n = 5  # hackish - lower "preamble" for the example test to work

for *pre, target in chunks(numbers, chunk_size=n + 1, overlap=n):
    if find_pair(Counter(pre), target) is None:
        print("part a:", target)
        break

start = stop = total = 0
while total != target:
    if total < target:
        total += numbers[stop]
        stop += 1
    else:
        total -= numbers[start]
        start += 1
chunk = numbers[start:stop]
print("part b:", min(chunk) + max(chunk))
