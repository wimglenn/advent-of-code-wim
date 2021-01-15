"""
--- Day 19: Go With The Flow ---
https://adventofcode.com/2018/day/19
"""
import math
from aocd import data
from aoc_wim.aoc2018.q16 import all_ops


def parsed(data):
    lines = data.splitlines()
    ip = int(lines.pop(0).split()[1])
    lines = [s.split() for s in lines]
    lines = [[a, int(b), int(c), int(d)] for a, b, c, d in lines]
    return ip, lines


funcs = all_ops()


class Comp:
    def __init__(self, ip, d, r0, hacked):
        self.hacked = hacked
        self.ip = ip
        self.i = 0
        self.d = d
        self.r = [0] * 6
        self.r[0] = r0

    def step(self):
        opname, a, b, c = self.d[self.i]
        op = funcs[opname]
        self.r[self.ip] = self.i
        op(self.r, a, b, c)
        self.r[self.ip] += 1
        self.i = self.r[self.ip]
        if self.hacked and self.i == 1 and max(self.r) > 5:
            self.r[0] = sum(divisors(max(self.r)))
            [][0]


def compute(data, r0=0, hack=False):
    ip, lines = parsed(data)
    comp = Comp(ip, lines, r0=r0, hacked=hack)
    while True:
        try:
            comp.step()
        except IndexError:
            break
    return comp.r[0]


def divisors(n):
    divs = {1, n}
    for i in range(2, int(math.sqrt(n)) + 1):
        if not n % i:
            divs |= {i, n // i}
    return divs


print("part a:", compute(data, r0=0, hack=True))
print("part b:", compute(data, r0=1, hack=True))
