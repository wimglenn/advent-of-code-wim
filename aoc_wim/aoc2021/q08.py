"""
--- Day 8: Seven Segment Search ---
https://adventofcode.com/2021/day/8
"""
from aocd import data
from itertools import permutations

segments = {
    1: "cf",
    7: "acf",
    4: "bcdf",
    8: "abcdefg",

    2: "acdeg",
    3: "acdfg",
    5: "abdfg",

    6: "abdefg",
    9: "abcdfg",
    0: "abcefg",
}

lookup = {frozenset(v): str(k) for k, v in segments.items()}
translations = [str.maketrans("".join(p), "abcdefg") for p in permutations("abcdefg", 7)]

a = b = 0
for line in data.splitlines():
    patterns, code = line.split(" | ")
    for part in code.split():
        a += len(part) in {2, 3, 4, 7}
    for t in translations:
        if all(frozenset(w.translate(t)) in lookup for w in patterns.split()):
            break
    code = "".join([lookup[frozenset(n.translate(t))] for n in code.split()])
    b += int(code)

print("part a:", a)
print("part b:", b)
