from aocd import data
from collections import defaultdict
from parse import parse
from types import SimpleNamespace
import operator as op

ops = {
    '>': op.gt,
    '<': op.lt,
    '>=': op.ge,
    '<=': op.le,
    '==': op.eq,
    '!=': op.ne,
    'inc': op.iadd,
    'dec': op.isub,
}

template = '{x} {i:op} {m:d} if {y} {cmp:op} {n:d}'

def run(data):
    b = 0
    d = defaultdict(int)
    for line in data.splitlines():
        r = SimpleNamespace(**parse(template, line, {'op': ops.get}).named)
        d[r.x] = r.i(d[r.x], r.cmp(d[r.y], r.n) and r.m)
        b = max(b, d[r.x])
    return max(d.values()), b

test_data = """\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""

assert run(test_data) == (1, 10)

a, b = run(data)
print("part a:", a)
print("part b:", b)
