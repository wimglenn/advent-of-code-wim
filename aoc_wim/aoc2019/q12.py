"""
--- Day 12: The N-Body Problem ---
https://adventofcode.com/2019/day/12
"""
import re
from itertools import count
from math import lcm

import numpy as np
from aocd import data


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


test10 = """\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

test100 = """\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""


n = 10 if data == test10 else 100 if data == test100 else 1000
print("answer_a:", simulate(data, n))
print("answer_b:", simulate(data))
