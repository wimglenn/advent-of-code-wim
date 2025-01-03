"""
--- Day 10: Elves Look, Elves Say ---
https://adventofcode.com/2015/day/10
"""
from itertools import groupby

from aocd import data
from aocd import extra


def look_and_say(s, n=1):
    for i in range(n):
        s = "".join([f"{len(list(group))}{key}" for key, group in groupby(s)])
    return s


n = extra.get("iterations", 40)
a = look_and_say(data, n=n)
print("answer_a:", len(a))
if not extra:
    b = look_and_say(a, n=50 - n)
    print("answer_b:", len(b))
