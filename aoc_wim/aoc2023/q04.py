"""
--- Day 4: Scratchcards ---
https://adventofcode.com/2023/day/4
"""
from aocd import data

lines = data.splitlines()
cards = [1] * len(lines)
a = 0
for i, line in enumerate(lines):
    L, R = line.split("|")
    w = {*L.split()} & {*R.split()}
    a += int(2 ** (len(w) - 1))
    for j in range(min(len(w), len(cards))):
        cards[i + 1 + j] += cards[i]

print("answer_a:", a)
print("answer_b:", sum(cards))
