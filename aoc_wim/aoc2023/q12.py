"""
--- Day 12: Hot Springs ---
https://adventofcode.com/2023/day/12
"""
from functools import cache

from aocd import data


@cache
def fits(ss, cs, h=0):
    if not any(cs):
        return "#" not in ss
    if not ss:
        return 0
    c, cs = cs[-1], cs[:-1]
    s, ss = ss[-1], ss[:-1]
    if not c:
        return (s != "#") and fits(ss, cs, 0)
    if h:
        return (s != ".") and fits(ss, (*cs, c-1), 1)
    if s == "#":
        return fits(ss, (*cs, c - 1), 1)
    if s == ".":
        return fits(ss, (*cs, c), 0)
    if s == "?":
        return fits(ss, (*cs, c), 0) + fits(ss, (*cs, c - 1), 1)


a = b = 0
for line in data.splitlines():
    template_a, counts = line.split()
    counts_a = *map(int, counts.split(",")),
    template_b = "?".join([template_a]*5)
    counts_b = counts_a*5
    a += fits(template_a, counts_a)
    b += fits(template_b, counts_b)
    fits.cache_clear()

print("answer_a:", a)
print("answer_b:", b)
