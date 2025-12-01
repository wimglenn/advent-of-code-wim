"""
--- Day 1: Secret Entrance ---
https://adventofcode.com/2025/day/1
"""

from aocd import data


a = b = 0
pos = 50
for n in map(int, data.replace("R", "").replace("L", "-").split()):
    d = -1 if n < 0 else 1
    q, n = divmod(n, d * 100)
    b += q
    for i in range(abs(n)):
        pos += d
        b += pos % 100 == 0
    a += pos % 100 == 0
print("answer_a:", a)
print("answer_b:", b)
