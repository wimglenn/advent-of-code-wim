"""
--- Day 17: No Such Thing as Too Much ---
https://adventofcode.com/2015/day/17
"""
from aocd import data
from aocd import extra

from aoc_wim.stuff import subset_sum


vals = [*map(int, data.split())]
subsets = list(subset_sum(vals, extra.get("liters", 150)))
print("answer_a:", len(subsets))
fewest = min(subsets, key=len)
print("answer_b:", sum(len(s) == len(fewest) for s in subsets))
