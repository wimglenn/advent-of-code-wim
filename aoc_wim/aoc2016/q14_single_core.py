"""
--- Day 14: One-Time Pad ---
https://adventofcode.com/2016/day/14
"""
import re
from collections import defaultdict
from aocd import data
from _md5 import md5


def search(data, stretch):
    template = data.encode() + b"%d"
    keys = []
    triples = defaultdict(list)
    pat3 = re.compile(r"(.)\1{2}")
    pat5 = re.compile(r"(.)\1{4}")
    i = 0
    stop = None
    while stop is None or i < stop:
        s = template % i
        for _ in range(stretch):
            s = md5(s).hexdigest().encode()
        s = s.decode()
        triple = pat3.search(s)
        if triple is not None:
            for quintuple in pat5.findall(s):
                keys.extend([x for x in triples[quintuple] if i - x <= 1000])
                triples[quintuple].clear()  # avoid to count same key twice
                if stop is None and len(keys) >= 64:
                    stop = i + 1001
            triples[triple.group()[0]].append(i)
        i += 1
    return sorted(keys)[63]


print("part a:", search(data, stretch=1))
print("part b:", search(data, stretch=2017))
