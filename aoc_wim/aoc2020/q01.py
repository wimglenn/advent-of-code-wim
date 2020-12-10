"""
--- Day 1: Report Repair ---
https://adventofcode.com/2020/day/1
"""
from collections import Counter
from aocd import data
from aoc_wim.aoc2020 import find_pair


counter = Counter(int(x) for x in data.splitlines())
x, y = find_pair(counter)
print(f"part a: {x} * {y} == {x * y}")

for z in list(counter):
    counter[z] -= 1
    try:
        x, y = find_pair(counter, target=2020 - z)
    except TypeError:
        counter[z] += 1
    else:
        assert x + y + z == 2020
        print(f"part b: {x} * {y} * {z} == {x * y * z}")
        break
