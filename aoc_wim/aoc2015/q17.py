"""
--- Day 17: No Such Thing as Too Much ---
https://adventofcode.com/2015/day/17
"""
from aocd import data

from aoc_wim.stuff import subset_sum

vals = [int(n) for n in data.splitlines()]
liters = 25 if len(vals) == 5 else 150
subsets = list(subset_sum(vals, liters))
print("answer_a:", len(subsets))
fewest = min(subsets, key=len)
print("answer_b:", sum(len(s) == len(fewest) for s in subsets))
