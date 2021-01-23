"""
--- Day 5: Alchemical Reduction ---
https://adventofcode.com/2018/day/5
"""
from aocd import data


def react(data):
    result = []
    for char in data:
        if result and char == result[-1].swapcase():
            result.pop()
        else:
            result.append(char)
    return "".join(result)


print("part a:", len(react(data)))

min_len = len(data)
for x in set(data.lower()):
    r = react(data.replace(x, "").replace(x.upper(), ""))
    min_len = min(len(r), min_len)

print("part b:", min_len)
