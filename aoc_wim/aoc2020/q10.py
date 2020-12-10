"""
--- Day 10: Adapter Array ---
https://adventofcode.com/2020/day/10
"""
from aocd import data
from aoc_wim.stuff import Tribonacci

numbers = [int(x) for x in data.split()]
numbers.append(0)  # outlet
numbers.sort()
numbers.append(numbers[-1] + 3)  # device
s0 = s = "".join([str(y - x) for x, y in zip(numbers, numbers[1:])])
print("part a:", s.count("1") * s.count("3"))

# find longest sequence of 1
i = 1
while "1" * i in s0:
    i += 1
tri = Tribonacci()

b = 1
while i > 1:
    substring = "1" * (i - 1)
    if substring in s:
        b *= tri[i + 1] ** s.count(substring)
        s = s.replace(substring, "")
    i -= 1
print("part b:", b)
