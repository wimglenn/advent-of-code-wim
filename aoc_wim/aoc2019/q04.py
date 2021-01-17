"""
--- Day 4: Secure Container ---
https://adventofcode.com/2019/day/4
"""
from aocd import data


def ok(n, part="a"):
    # It is a six-digit number.
    if not (100_000 <= n <= 999_999):
        return False

    # Two adjacent digits are the same. (part a)
    # ... but not part of a larger group of matching digits (part b)
    str_n = str(n)
    for s in "0123456789":
        if 2 * s in str_n:
            if part == "a":
                break
            elif part == "b" and 3 * s not in str_n:
                break
    else:
        return False

    # Going from left to right, the digits never decrease
    for i in range(5):
        if str_n[i + 1] < str_n[i]:
            return False

    return True


lo, hi = data.split("-")
ns = range(int(lo), int(hi) + 1)

print("part a:", sum(ok(n, part="a") for n in ns))
print("part b:", sum(ok(n, part="b") for n in ns))
