"""
--- Day 10: Adapter Array ---
https://adventofcode.com/2020/day/10
"""
from aocd import numbers

numbers.sort()
d1 = d3 = prev = 0
for n in numbers:
    d1 += n - prev == 1
    d3 += n - prev == 3
    prev = n
d3 += 1  # extra hop to device
print("part a:", d1 * d3)

memo = {0: 1}
for n in numbers:
    memo[n] = sum(memo.get(n - i, 0) for i in range(4))

print("part b:", memo[n])
