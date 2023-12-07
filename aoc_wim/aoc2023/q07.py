"""
--- Day 7: Camel Cards ---
https://adventofcode.com/2023/day/7
"""
from aocd import data
from collections import Counter
from itertools import combinations_with_replacement


cards = "AKQJT98765432"
tr = str.maketrans("TQKA", "IKLM")


def key_a(hand):
    return sorted(Counter(hand).values(), reverse=True), hand.translate(tr)


def key_b(hand):
    hands = [hand]
    for comb in combinations_with_replacement(cards, hand.count("J")):
        it = iter(comb)
        hands.append("".join([next(it) if h == "J" else h for h in hand]))
        assert next(it, None) is None
    k0, _k1 = max(key_a(c) for c in hands)
    return k0, hand.translate(tr).replace("J", "0")


d = dict(h.split() for h in data.splitlines())
print("answer_a", sum(i * int(d[k]) for i, k in enumerate(sorted(d, key=key_a), 1)))
print("answer_b", sum(i * int(d[k]) for i, k in enumerate(sorted(d, key=key_b), 1)))
