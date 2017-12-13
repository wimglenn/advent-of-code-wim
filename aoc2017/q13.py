from aocd import data
from parse import parse
from itertools import count

test_data = '''0: 3
1: 2
4: 4
6: 4'''

def parsed(data):
    d = {}
    for line in data.splitlines():
        result = parse('{depth:d}: {range:d}', line)
        d[result.named['depth']] = 2*result.named['range']-2
    return d

def severity(delay=0):
    return sum(t*(r+2)//2 for t, r in d.items() if (t+delay) % r == 0)

def delay():
    for t0 in count():
        s = severity(delay=t0)
        if not s and t0 % d[0]:
            return t0

d = parsed(test_data)
assert severity() == 24
assert delay() == 10

d = parsed(data)
print(severity())  # part a: 1316
print(delay())  # part b: 3840052
