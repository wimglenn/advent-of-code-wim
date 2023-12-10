"""
--- Day 7: Camel Cards ---
https://adventofcode.com/2023/day/7
"""
from collections import Counter

from aocd import data


tr = str.maketrans("TQKA", "IKLM")


def key_a(h):
    return sorted(Counter(h[0]).values(), reverse=True), h[0].translate(tr)


def key_b(h):
    c = Counter(h[0].replace("J", "") or "J")
    k0, _ = key_a([h[0].replace("J", max(c, key=c.get))])
    return k0, h[0].translate(tr).replace("J", "0")


d = [h.split() for h in data.splitlines()]
print("answer_a", sum(i * int(b) for i, (h, b) in enumerate(sorted(d, key=key_a), 1)))
print("answer_b", sum(i * int(b) for i, (h, b) in enumerate(sorted(d, key=key_b), 1)))
