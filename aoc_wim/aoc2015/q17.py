"""
--- Day 17: No Such Thing as Too Much ---
https://adventofcode.com/2015/day/17
"""
from collections import Counter

from aocd import data

from aoc_wim.stuff import subset_sum


vals = [int(n) for n in data.splitlines()]
liters = 25 if len(vals) == 5 else 150
subsets = list(subset_sum(vals, liters))
print("part a:", len(subsets))
fewest = min(subsets, key=len)
print("part b:", sum(len(s) == len(fewest) for s in subsets))
