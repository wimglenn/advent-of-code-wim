"""
--- Day 10: Elves Look, Elves Say ---
https://adventofcode.com/2015/day/10
"""
from itertools import groupby

from aocd import data


def look_and_say(s, n=1):
    for i in range(n):
        s = "".join([f"{len(list(group))}{key}" for key, group in groupby(s)])
    return s


if __name__ == "__main__":
    a = look_and_say(data, n=40)
    print("part a:", len(a))
    b = look_and_say(a, n=50 - 40)
    print("part b:", len(b))
