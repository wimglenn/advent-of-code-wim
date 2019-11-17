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


def exe(data):
    b = 0
    d = defaultdict(int)
    template = "{x} {i:op} {m:d} if {y} {cmp:op} {n:d}"
    for line in data.splitlines():
        parsed = parse(template, line, {"op": ops.get})
        r = SimpleNamespace(**parsed.named)
        d[r.x] = r.i(d[r.x], r.cmp(d[r.y], r.n) and r.m)
        b = max(b, d[r.x])
    return max(d.values()), b


test_data = """\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
assert exe(test_data) == (1, 10)

a, b = exe(data)
print("part a:", a)
print("part b:", b)
