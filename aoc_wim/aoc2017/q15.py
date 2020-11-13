"""
--- Day 15: Dueling Generators ---
https://adventofcode.com/2017/day/15
"""
from aocd import data
from parse import parse

a = 16807  # 7 ** 5
b = 48271  # prime
d = 2147483647  # prime

template = "Generator A starts with {:d}\nGenerator B starts with {:d}"
a0, b0 = parse(template, data).fixed  # note: a0 is 2**n, b0 is prime


def gen(m, x0):
    x = x0
    while True:
        x = (x * m) % d
        yield x


def gen2(m, x0, d):
    for x in gen(m, x0):
        if x % d == 0:
            yield x


def score(gena, genb, n=40000000):
    x = 0
    for i in range(n):
        a, b = next(gena), next(genb)
        x += a & 0xFFFF == b & 0xFFFF
    return x


print(score(gen(a, a0), gen(b, b0)))
print(score(gen2(a, a0, 4), gen2(b, b0, 8), n=5000000))
