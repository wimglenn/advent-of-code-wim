from aocd import data
from itertools import count
import numpy as np
import re


def gcd(a, b):
    """greatest common divisor"""
    return gcd(b, a % b) if b else a


def lcm(a, b):
    """least common multiple"""
    return abs(a * b) // gcd(a, b)


def simulate(data, n=0):
    ns = re.findall(r"-?\d+", data)
    p = np.array([int(n) for n in ns]).reshape(-1, 3)
    v = np.zeros_like(p)

    tx = None
    ty = None
    tz = None
    seenx = {}
    seeny = {}
    seenz = {}

    for t in range(n) or count():

        sx = tuple(p[:, 0]) + tuple(v[:, 0])
        sy = tuple(p[:, 1]) + tuple(v[:, 1])
        sz = tuple(p[:, 2]) + tuple(v[:, 2])
        if sx in seenx:
            tx = t - seenx[sx]
        seenx[sx] = t
        if sy in seeny:
            ty = t - seeny[sy]
        seeny[sy] = t
        if sz in seenz:
            tz = t - seenz[sz]
        seenz[sz] = t
        if tx is not None and ty is not None and tz is not None:
            return lcm(tx, lcm(ty, tz))

        for p0, v0 in zip(p, v):
            v0 += (p0 < p).sum(axis=0) - (p0 > p).sum(axis=0)
        p += v

    pe = abs(p).sum(axis=1)
    ke = abs(v).sum(axis=1)
    e = (pe * ke).sum()
    return e


test1 = """\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

test2 = """\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""


assert simulate(test1, n=10) == 179
assert simulate(test2, n=100) == 1940
print(simulate(data, n=1000))

assert simulate(test1) == 2772
assert simulate(test2) == 4686774924
print(simulate(data))
