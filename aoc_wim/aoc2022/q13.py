"""
--- Day 13: Distress Signal ---
https://adventofcode.com/2022/day/13
"""
from aocd import data
from ast import literal_eval
from functools import cmp_to_key


def cmp(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return -1 if a < b else 0 if a == b else 1
    if isinstance(a, list) and isinstance(b, list):
        for x, y in zip(a, b):
            if c := cmp(x, y):
                return c
        return cmp(len(a), len(b))
    if isinstance(a, list) and isinstance(b, int):
        return cmp(a, [b])
    elif isinstance(a, int) and isinstance(b, list):
        return cmp([a], b)


a = 0
packets = []
for i, chunk in enumerate(data.split("\n\n"), 1):
    first, second = map(literal_eval, chunk.splitlines())
    packets += [first, second]
    if cmp(first, second) == -1:
        a += i

packets += [[], [[2]], [[6]]]
packets.sort(key=cmp_to_key(cmp))
b = packets.index([[2]]) * packets.index([[6]])

print("part a:", a)
print("part b:", b)
