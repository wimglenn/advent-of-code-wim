"""
--- Day 15: Rambunctious Recitation ---
https://adventofcode.com/2020/day/15
"""
from aocd import data


# CPython hack: loading names in a local namespace (LOAD_FAST op) is
# quicker than loading names in a module namespace (LOAD_GLOBAL op)
def local(n):
    seen = {}
    get = seen.get
    for i0, prev in enumerate(ns, start=1):
        seen[prev] = i0
    for i in range(i0, n):
        seen[prev], prev = i, i - get(prev, i)
    return prev


ns = [int(x) for x in data.split(",")]
print("part a:", local(2020))
print("part b:", local(30000000))
