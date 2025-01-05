"""
--- Day 7: Bridge Repair ---
https://adventofcode.com/2024/day/7
"""
from math import log10

from aocd import data


def possible(target, ns, part="a"):
    *ns, n = ns
    if not ns:
        return n == target
    if part == "b":
        q, r = divmod(target, 10 ** (1 + int(log10(n))))
        if r == n and possible(q, ns, part):
            return True
    q, r = divmod(target, n)
    if r == 0 and possible(q, ns, part):
        return True
    return possible(target - n, ns, part)


a = b = 0
for line in data.replace(":", "").splitlines():
    target, *ns = map(int, line.split())
    if possible(target, ns):
        a += target
        b += target
    elif possible(target, ns, part="b"):
        b += target


print("answer_a:", a)
print("answer_b:", b)
