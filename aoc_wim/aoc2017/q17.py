"""
--- Day 17: Spinlock ---
https://adventofcode.com/2017/day/17
"""
from aocd import data

n = int(data)

L = [0]
pos = 0
for i in range(1, 2017 + 1):
    pos = 1 + (pos + n) % i
    L.insert(pos, i)
print("part a:", L[pos + 1])

pos = 0
i = b = 1
while i <= 50000000:
    pos = 1 + (pos + n) % i
    if pos == 1:
        b = i
    # when pos is much smaller than i, we can skip
    # ahead iterations. as i gets bigger, this
    # becomes an increasingly effective speedup
    inci = (i - pos) // (n + 1) or 1
    pos += (n + 1) * (inci - 1)
    i += inci
print("part b:", b)
