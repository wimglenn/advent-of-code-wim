"""
--- Day 13: Distress Signal ---
https://adventofcode.com/2022/day/13
"""
from aocd import data
from json import loads
from functools import cmp_to_key


def cmp(a, b):
    match a, b:
        case int(), int():
            return a - b
        case list(), list():
            for x, y in zip(a, b):
                if c := cmp(x, y):
                    return c
            return cmp(len(a), len(b))
        case list(), int():
            return cmp(a, [b])
        case int(), list():
            return cmp([a], b)


a = 0
packets = []
for i, chunk in enumerate(data.split("\n\n"), 1):
    first, second = map(loads, chunk.splitlines())
    packets += [first, second]
    if cmp(first, second) < 0:
        a += i

packets += [[], [[2]], [[6]]]
packets.sort(key=cmp_to_key(cmp))
b = packets.index([[2]]) * packets.index([[6]])

print("part a:", a)
print("part b:", b)
