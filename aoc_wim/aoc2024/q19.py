"""
--- Day 19: Linen Layout ---
https://adventofcode.com/2024/day/19
"""
from aocd import data
from functools import cache


@cache
def ways(design):
    if not design:
        return 1
    return sum(ways(design[len(p):]) for p in patterns if design.startswith(p))


patterns, designs = data.split("\n\n")
patterns = patterns.split(", ")
results = [ways(d) for d in designs.split()]
print("answer_a:", sum(map(bool, results)))
print("answer_b:", sum(results))
