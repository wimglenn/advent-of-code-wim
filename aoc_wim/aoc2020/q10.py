"""
--- Day 10: Adapter Array ---
https://adventofcode.com/2020/day/10
"""
from aocd import data
from aoc_wim.stuff import Tribonacci

numbers = [int(x) for x in data.split()]
numbers.append(0)  # outlet
numbers.sort()
Δ = [y - x for x, y in zip(numbers, numbers[1:])]
Δ.append(3)  # device
print("part a:", Δ.count(1) * Δ.count(3))

tri = Tribonacci()
Π = 1
ones = 0
for d in Δ:
    if d == 1:
        ones += 1  # finding longest streak of ones
        continue
    Π *= tri[ones + 2] or 1  # streak broken, cash in
    ones = 0
print("part b:", Π)
