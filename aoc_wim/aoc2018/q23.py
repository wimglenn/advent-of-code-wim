"""
--- Day 23: Experimental Emergency Teleportation ---
https://adventofcode.com/2018/day/23
"""
from heapq import heappop
from heapq import heappush
from itertools import product

import math
import numpy as np
from aocd import data
from parse import parse


def parsed(data):
    template = "pos=<{:d},{:d},{:d}>, r={:d}"
    nums = [parse(template, s).fixed for s in data.splitlines()]
    A = np.array(nums)
    xs = A[:, :-1]
    rs = A[:, -1]
    return xs, rs


class Cell:
    def __init__(self, x, s):
        self.x = x  # 3d position of corner
        self.s = s  # edge size
        lo = np.maximum(self.x - xs, 0)
        hi = np.maximum(xs - self.x - self.s, 0)
        self.n_out = ((lo + hi).sum(axis=1) > rs).sum()  # count bots out of range
        self.d = abs(self.x).sum()  # manhattan distance of corner from origin

    def split(self):
        # divide this 3D space into 8 evenly sized subspaces
        # see https://en.wikipedia.org/wiki/Octree for inspiration
        halfwidth = self.s // 2
        dx = np.array(list(product([0, 1], repeat=3))) * halfwidth
        for x in self.x + dx:
            yield Cell(x, halfwidth)

    def __lt__(self, other):
        # key for heapq comparison - we will minimise over tuples of:
        # (number of bots outside, cell edge size, distance of the corner from origin)
        # maximize number in range = minimizing number out of range
        return (self.n_out, self.s, self.d) < (other.n_out, other.s, other.d)


xs, rs = parsed(data)
i = rs.argmax()
print("part a:", (abs(xs - xs[i]).sum(axis=1) <= rs[i]).sum())

x0 = 2 ** math.ceil(math.log2(abs(xs).max()))
cell = Cell(x=np.array([-x0, -x0, -x0]), s=x0 * 2)
assert cell.n_out == 0, "initial cell must cover all bots"

pq = [cell]
while pq:
    cell = heappop(pq)
    print(f"qlen={len(pq)} s={cell.s} {len(xs) - cell.n_out} nanobots")
    if not cell.s:
        break
    for subcell in cell.split():
        heappush(pq, subcell)
print("part b:", cell.d)
