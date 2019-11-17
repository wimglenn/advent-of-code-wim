from types import SimpleNamespace

import numpy as np
from aocd import data
from parse import parse


def part_ab(data):
    template = "#{id:d} @ {col:d},{row:d}: {w:d}x{h:d}"
    claims = [SimpleNamespace(**parse(template, s).named) for s in data.splitlines()]
    W = max(c.col + c.w for c in claims)
    H = max(c.row + c.h for c in claims)
    A = np.zeros((H, W, len(claims)), dtype=int)
    for c in claims:
        A[c.row : c.row + c.h, c.col : c.col + c.w, c.id - 1] = 1
    part_a = (A.sum(axis=2) > 1).sum()
    for c in claims:
        if A[c.row : c.row + c.h, c.col : c.col + c.w, :].sum() == c.w * c.h:
            return part_a, c.id


test_data = """\
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2"""

assert part_ab(test_data) == (4, 3)


a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
