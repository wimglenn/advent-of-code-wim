"""
--- Day 4: High-Entropy Passphrases ---
https://adventofcode.com/2017/day/4
"""
from aocd import data


def has_dupe(txt):
    parts = txt.split()
    return len(parts) != len(set(parts))


def has_anagram(txt):
    parts = [tuple(sorted(x)) for x in txt.split()]
    return len(parts) != len(set(parts))


a = b = 0
for txt in data.splitlines():
    a += not has_dupe(txt)
    b += not has_anagram(txt)

print("part a:", a)
print("part b:", b)
