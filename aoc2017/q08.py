from aocd import data
from collections import defaultdict
from parse import parse
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

template = '{x} {iop} {m:d} if {y} {cmp} {n:d}'

def run(data):
    b = 0
    d = defaultdict(int)
    for line in data.splitlines():
        r = parse(template, line).named
        d[r['x']] = ops[r['iop']](d[r['x']], ops[r['cmp']](d[r['y']], r['n']) and r['m'])
        b = max(b, d[r['x']])
    return max(d.values()), b

test_data = '''b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10'''

assert run(test_data) == (1, 10)
a, b = run(data)
print(a)  # part a: 4448
print(b)  # part b: 6582
