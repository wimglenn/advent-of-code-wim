"""
--- Day 4: Scratchcards ---
https://adventofcode.com/2023/day/4
"""
from aocd import data

lines = data.splitlines()
n = len(lines)
L = [1] * n
a = b = 0
for i, line in enumerate(lines):
    _, lr = line.split(": ")
    l, r = lr.split(" | ")
    winners = {int(x) for x in l.split()}
    w = sum(1 for i in map(int, r.split()) if i in winners)
    if w:
        a += 2 ** (w - 1)
    b += L[i]
    for j in range(i + 1, i + 1 + w):
        try:
            L[j] += L[i]
        except IndexError:
            break

print("answer_a:", a)
print("answer_b:", b)
