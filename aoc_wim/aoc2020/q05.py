"""
--- Day 5: Binary Boarding ---
https://adventofcode.com/2020/day/5
"""
from aocd import data

tr = str.maketrans("FBLR", "0101")
ids = {int(x.translate(tr), 2) for x in data.splitlines()}
print(max(ids))
missing = set(range(min(ids), max(ids))) - ids
print(*missing)
