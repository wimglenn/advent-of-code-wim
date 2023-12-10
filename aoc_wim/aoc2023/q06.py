"""
--- Day 6: Wait For It ---
https://adventofcode.com/2023/day/6
"""
from math import prod
from math import sqrt

from aocd import data


def quadratic(t, d):
    return t - 1 - 2*int(t/2 - sqrt(t*t - 4*d)/2)


ts, ds = data.splitlines()
ts = ts.split()[1:]
ds = ds.split()[1:]

print("answer_a:", prod(quadratic(int(t), int(d)) for t, d in zip(ts, ds)))
print("answer_b:", quadratic(int("".join(ts)), int("".join(ds))))
