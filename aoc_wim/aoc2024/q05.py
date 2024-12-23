"""
--- Day 5: Print Queue ---
https://adventofcode.com/2024/day/5
"""
from aocd import data
from collections import defaultdict
from functools import cmp_to_key


rules, updates = data.split("\n\n")
rules = [x.split("|") for x in rules.splitlines()]
updates = [x.split(",") for x in updates.splitlines()]

d = defaultdict(set)
for left, right in rules:
    d[left].add(right)


def cmp(p1, p2):
    if p2 in d.get(p1, []):
        return -1
    if p1 in d.get(p2, []):
        return 1
    return 0


a = b = 0
for update in updates:
    pages = sorted(update, key=cmp_to_key(cmp))
    mid = int(pages[len(pages) // 2])
    if pages == update:
        a += mid
    else:
        b += mid

print("answer_a:", a)
print("answer_b:", b)
