"""
--- Day 12: The N-Body Problem ---
https://adventofcode.com/2019/day/12
"""
from aocd import data
from itertools import count
from math import lcm
import numpy as np
import re


def simulate(data, n=0):
    p = np.array(re.findall(r"-?\d+", data)).astype(int).reshape(-1, 3)
    v = np.zeros_like(p)

    ts = [0, 0, 0]
    ss = [(p[:, i].tobytes(), v[:, i].tobytes()) for i in range(3)]
    for t in range(n) or count():

        for i in range(3):
            if not ts[i]:
                s = p[:, i].tobytes(), v[:, i].tobytes()
                if s == ss[i]:
                    ts[i] = t
                    if all(ts):
                        tx, ty, tz = ts
                        return lcm(tx, ty, tz)

        v += np.sign(p[:, None, :] - p).sum(axis=0)
        p += v

    pe = abs(p).sum(axis=1)
    ke = abs(v).sum(axis=1)
    e = (pe * ke).sum()
    return e


print("part a:", simulate(data, n=1000))
print("part b:", simulate(data))
