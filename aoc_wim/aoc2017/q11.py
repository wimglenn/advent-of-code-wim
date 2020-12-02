"""
--- Day 11: Hex Ed ---
https://adventofcode.com/2017/day/11
"""
from collections import Counter

from aocd import data


def norm(data, steps=None):
    c = Counter(data.split(",")[:steps])
    c["ne"] -= c.pop("sw", 0)
    c["nw"] -= c.pop("se", 0)
    c["s"] -= c.pop("n", 0)
    d = sum(abs(x) for x in c.values()) - abs(sorted(c.values())[1])
    return d


print(norm(data))
print(max(norm(data, steps=i) for i in range(data.count(","))))
