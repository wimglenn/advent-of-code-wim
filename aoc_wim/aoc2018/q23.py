from heapq import heappop
from heapq import heappush
from itertools import product

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


def part_a(data):
    xs, rs = parsed(data)
    i = rs.argmax()
    return (abs(xs - xs[i]).sum(axis=1) <= rs[i]).sum()


def part_b(data):
    xs, rs = parsed(data)
    x0 = xs.min(axis=0)
    priority_queue = [(0, xs.ptp(axis=0).max(), abs(x0).sum(), *x0)]
    while priority_queue:
        n_out_of_range, s, d, *x = heappop(priority_queue)
        x = np.array(x)
        s //= 2
        if not s:
            x0 = x
            # return d
            break
        dx = np.array(list(product([0, 1], repeat=3))) * s
        # divide this 3D space into 8 evenly sized subspaces
        for row in x + dx:
            # maximize number in range = minimizing number out of range
            lo = np.clip(row - xs, 0, None)
            hi = np.clip(xs - row - s + 1, 0, None)
            n_out = ((lo + hi).sum(axis=1) > rs).sum()
            if n_out < len(rs):
                heappush(priority_queue, (n_out, s, abs(row).sum(), *row))
    # search around neighborhood of x0
    r = 8
    for dx in product(range(-r, r + 1), repeat=3):
        dx = np.array(dx)
        x = x0 + dx
        n_out = (abs(xs - x).sum(axis=1) > rs).sum()
        n_out_of_range, d = min((n_out_of_range, d), (n_out, abs(x).sum()))
    return d


test_data_a = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1"""

test_data_b = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""


assert part_a(test_data_a) == 7
assert part_b(test_data_b) == 36


print("part a:", part_a(data))
print("part b:", part_b(data))
