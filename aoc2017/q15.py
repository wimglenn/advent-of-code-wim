from aocd import data
from parse import parse

a = 16807
b = 48271
d = 2147483647

parsed = parse('Generator A starts with {a0:d}\nGenerator B starts with {b0:d}', data)
a0 = parsed.named['a0']
b0 = parsed.named['b0']

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
        x += a & 0xffff == b & 0xffff
    return x

assert score(gen(a, 65), gen(b, 8921)) == 588
assert score(gen2(a, 65, 4), gen2(b, 8921, 8), n=5000000) == 309

print(score(gen(a, a0), gen(b, b0)))
print(score(gen2(a, a0, 4), gen2(b, b0, 8), n=5000000))
