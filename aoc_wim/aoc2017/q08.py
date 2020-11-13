"""
--- Day 8: I Heard You Like Registers ---
https://adventofcode.com/2017/day/8
"""
import operator as op
from collections import defaultdict
from types import SimpleNamespace

from aocd import data
from parse import parse


ops = {
    ">": op.gt,
    "<": op.lt,
    ">=": op.ge,
    "<=": op.le,
    "==": op.eq,
    "!=": op.ne,
    "inc": op.iadd,
    "dec": op.isub,
}


b = 0
d = defaultdict(int)
template = "{x} {i:op} {m:d} if {y} {cmp:op} {n:d}"
for line in data.splitlines():
    parsed = parse(template, line, {"op": ops.get})
    r = SimpleNamespace(**parsed.named)
    d[r.x] = r.i(d[r.x], r.cmp(d[r.y], r.n) and r.m)
    b = max(b, d[r.x])


print("part a:", max(d.values()))
print("part b:", b)
