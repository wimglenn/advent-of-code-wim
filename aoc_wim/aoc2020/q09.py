"""
--- Day 9: Encoding Error ---
https://adventofcode.com/2020/day/9
"""
from aocd import data

from aoc_wim.aoc2020 import find_pair

numbers = [int(x) for x in data.splitlines()]
n = 25
if len(numbers) < n:
    n = 5  # hackish - lower "preamble" for the example test to work

pre = set(numbers[:n])
for i in range(n, len(numbers)):
    target = numbers[i]
    if find_pair(pre, target) is None:
        print("answer_a:", target)
        break
    pre.remove(numbers[i - n])
    pre.add(target)

start = 0
stop = 2
total = sum(numbers[start:stop])
while total != target or start == stop - 1:
    if total < target:
        total += numbers[stop]
        stop += 1
    else:
        total -= numbers[start]
        start += 1
chunk = numbers[start:stop]
assert sum(chunk) == target, "the chunk must sum to the target value"
assert len(chunk) >= 2, "the chunk must be a contiguous set of at least two numbers"
print("answer_b:", min(chunk) + max(chunk))
