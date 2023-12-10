"""
--- Day 6: Signals and Noise ---
https://adventofcode.com/2016/day/6
"""
from collections import Counter

from aocd import data

counters = [Counter(x) for x in zip(*data.splitlines())]
print("answer_a:", "".join([max(c, key=c.get) for c in counters]))
print("answer_b:", "".join([min(c, key=c.get) for c in counters]))
