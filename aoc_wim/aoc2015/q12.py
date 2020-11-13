"""
--- Day 12: JSAbacusFramework.io ---
https://adventofcode.com/2015/day/12
"""
import json
import re

from aocd import data


def sum_of_numbers_in_text(s):
    return sum(int(n) for n in re.findall(r"-?\d+", s))


def rsum(data):
    if isinstance(data, int):
        return data
    elif isinstance(data, dict):
        if "red" in data.values():
            return 0
        return rsum(list(data.values()))
    elif isinstance(data, list):
        return sum(rsum(n) for n in data)
    else:
        return 0


print(sum_of_numbers_in_text(data))
print(rsum(json.loads(data)))
