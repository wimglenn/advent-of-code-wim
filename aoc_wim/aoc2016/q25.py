"""
--- Day 25: Clock Signal ---
https://adventofcode.com/2016/day/25
"""
import re
from aocd import data

x, y = re.findall(r"\d+", data)[:2]
a = 0b101010101010 - int(x) * int(y)
print("part a:", a)
