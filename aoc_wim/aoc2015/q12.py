"""
--- Day 12: JSAbacusFramework.io ---
https://adventofcode.com/2015/day/12
"""
import json
import re

from aocd import data


def numbers(s):
    return re.findall(r"-?\d+", s)


def rsum(data):
    match data:
        case int(): return data
        case list(): return sum(rsum(x) for x in data)
        case dict():
            vals = list(data.values())
            return 0 if "red" in vals else rsum(vals)
        case _: return 0


print("answer_a:", sum(map(int, numbers(data))))
print("answer_b:", rsum(json.loads(data)))
