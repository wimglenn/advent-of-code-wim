"""
--- Day 2: Gift Shop ---
https://adventofcode.com/2025/day/2
"""

from aocd import data

ranges = [xy.split("-") for xy in data.split(",")]
ranges = [range(int(x), int(y) + 1) for x, y in ranges]
a = b = 0
for r in ranges:
    for n in r:
        s = str(n)
        w = len(s) // 2
        if s == s[:w] * 2:
            a += n
            b += n
        else:
            for i in range(1, w + 1):
                if s == s[:i] * (len(s) // i):
                    b += n
                    break
print("answer_a:", a)
print("answer_b:", b)
