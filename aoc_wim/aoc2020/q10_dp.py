"""
--- Day 10: Adapter Array ---
https://adventofcode.com/2020/day/10
"""
from aocd import data

ns = [*map(int, data.split())]
ns.sort()
d1 = d3 = prev = 0
for n in ns:
    d1 += n - prev == 1
    d3 += n - prev == 3
    prev = n
d3 += 1  # extra hop to device
print("answer_a:", d1 * d3)

memo = {0: 1}
for n in ns:
    memo[n] = sum(memo.get(n - i, 0) for i in range(4))

print("answer_b:", memo[n])
