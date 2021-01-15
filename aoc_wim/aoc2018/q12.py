"""
--- Day 12: Subterranean Sustainability ---
https://adventofcode.com/2018/day/12
"""
from aocd import data


def parsed(data):
    initial, _, *rest = data.splitlines()
    s0 = initial.split()[-1]
    p0 = s0.index("#")
    s0 = s0.strip(".")
    rules = dict(r.split(" => ") for r in rest)
    return s0, p0, rules


def mutate(s, p0, rules):
    s = "...." + s + "...."
    chunks = [s[i : i + 5] for i in range(len(s))]
    full = "".join([rules.get(c, ".") for c in chunks])
    p0 += full.index("#") - 2
    return full.strip("."), p0


def score(s, p0=0):
    return sum(i for i, v in enumerate(s, start=p0) if v == "#")


def part_a(data, n=20):
    s0, p0, rules = parsed(data)
    for i in range(n):
        s1, p1 = mutate(s0, p0, rules)
        if s1 == s0:
            return score(s1, p0=p1 + n - i - 1)
        s0, p0 = s1, p1
    return score(s0, p0)


def part_b(data):
    return part_a(data, n=50000000000)


print("part a:", part_a(data))
print("part b:", part_b(data))
