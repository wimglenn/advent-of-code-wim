"""
--- Day 5: Alchemical Reduction ---
https://adventofcode.com/2018/day/5
"""
from aocd import data


def react(data, remove=None):
    if remove is not None:
        data = data.replace(remove, "").replace(remove.swapcase(), "")
    result = []
    for char in data:
        if result and char == result[-1].swapcase():
            result.pop()
        else:
            result.append(char)
    return "".join(result)


print("part a:", len(react(data)))


def choices(data):
    units = set(data.lower())
    results = {u: react(data, remove=u) for u in units}
    return results


print("part b:", min([len(v) for v in choices(data).values()], default=0))
