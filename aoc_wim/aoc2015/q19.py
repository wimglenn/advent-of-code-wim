"""
--- Day 19: Medicine for Rudolph ---
https://adventofcode.com/2015/day/19
"""
from collections import defaultdict

from aocd import data


reactions, element = data.split("\n\n")
tr = defaultdict(list)
tri = {}
for line in reactions.splitlines():
    s, r = line.split(" => ")
    tr[s].append(r)
    tri[r] = s


seen = set()
for s, rs in tr.items():
    splitted = element.split(s)
    for i, (left, right) in enumerate(zip(splitted, splitted[1:])):
        for r in rs:
            new = splitted[:]
            new[i : i + 2] = [left + r + right]
            new = s.join(new)
            seen.add(new)


replacements = 0
while element != "e":
    pos = {}
    for k, v in tri.items():
        delta = len(k) - len(v)
        if k in element:
            if v != "e" or len(element) - delta == 1:
                pos[k] = (element.rfind(k) + len(k), delta)
    k = max(pos, key=pos.get)
    v = tri[k]
    # replace from right
    element = element[::-1].replace(k[::-1], v[::-1], 1)[::-1]
    replacements += 1


print("part a:", len(seen))
print("part b:", replacements)
