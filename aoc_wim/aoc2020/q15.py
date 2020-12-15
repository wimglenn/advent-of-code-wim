"""
--- Day 15: Rambunctious Recitation ---
https://adventofcode.com/2020/day/15
"""
from aocd import data


def local():
    i = 0
    seen = {}
    for s in data.split(","):
        i += 1
        prev = int(s)
        seen[prev] = i
    while True:
        if prev not in seen:
            n = 0
        else:
            n = i - seen[prev]
        seen[prev] = i
        prev = n
        i += 1
        if i == 2020:
            print("part a:", n)
        elif i == 30000000:
            print("part b:", n)
            break

# CPython hack: loading names in a local namespace is significantly faster than
# loading names from a global (module) namespace
local()
