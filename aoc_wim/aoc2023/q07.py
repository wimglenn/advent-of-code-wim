"""
--- Day 7: Camel Cards ---
https://adventofcode.com/2023/day/7
"""
from aocd import data
from collections import Counter


tr = str.maketrans("TQKA", "IKLM")


def key_a(hand):
    return sorted(Counter(hand).values(), reverse=True), hand.translate(tr)


def key_b(hand):
    h = hand.replace("J", "")
    best = hand.replace("J", max(h, key=h.count, default="J"))
    k0, _ = key_a(best)
    return k0, hand.translate(tr).replace("J", "0")


d = dict(h.split() for h in data.splitlines())
print("answer_a", sum(i * int(d[k]) for i, k in enumerate(sorted(d, key=key_a), 1)))
print("answer_b", sum(i * int(d[k]) for i, k in enumerate(sorted(d, key=key_b), 1)))
