"""
--- Day 9: Movie Theater ---
https://adventofcode.com/2025/day/9
"""

import heapq
from collections import defaultdict
from aocd import data


ns = [int(n) for n in data.replace(",", " ").split()]
zs = [complex(x, y) for x, y in zip(ns[0::2], ns[1::2])]
heap = []
a = 0
for i in range(len(zs)):
    for j in range(i + 1, len(zs)):
        dz = zs[i] - zs[j]
        area = int((abs(dz.real) + 1) * (abs(dz.imag) + 1))
        # negate area for a min heap (so we can pop largest rectangles first)
        heapq.heappush(heap, (-area, i, j))
        if area > a:
            a = area
print("answer_a:", a)


def hv(zs):
    # given a polygon determined by vertices in zs, return lists of horizontal
    # and vertical edges. the edge line segments are specified by two points.
    horizontals = []
    verticals = []
    for z0, z1 in zip(zs, zs[1:] + [zs[0]]):
        if z0.real == z1.real:
            if z0.imag > z1.imag:
                z0, z1 = z1, z0
            verticals.append((z0, z1))
        else:
            if z0.real > z1.real:
                z0, z1 = z1, z0
            horizontals.append((z0, z1))
    return horizontals, verticals


def crossing(hs, vs):
    for zh0, zh1 in hs:
        for zv0, zv1 in vs:
            if zh0.real < zv0.real < zh1.real and zv0.imag < zh0.imag < zv1.imag:
                return True
    return False


def interior_v(z, hs):
    # check if vertex z is inside the polygon
    # vertical ray casting - count crossings over horizontal edges hs
    zv0 = complex(z.real, 0)
    zv1 = z
    crossings = 0
    for zh0, zh1 in hs:
        if zh0.real <= zv0.real < zh1.real and zv0.imag <= zh0.imag < zv1.imag:
            crossings += 1
    return crossings % 2 == 1


def key(zs):
    # used to sort the longest edge lengths first.
    # the puzzle data has two massive horizontal lines which intersect with the
    # vertical edges of a large number of candidate rectangles.
    # pre-sorting gives the line intersection checks opportunity to exit earlier.
    z1, z0 = zs
    return -abs(z1 - z0)


Hs, Vs = hv(zs)
Hs.sort(key=key)
Vs.sort(key=key)
dH = defaultdict(list)
# build lookups for horizontal and vertical line segments, so we can efficiently
# test whether a given point lies on one of the polygon edges.
for z0, z1 in Hs:
    dH[z0.imag].append((z0, z1))
dV = defaultdict(list)
for z0, z1 in Vs:
    dV[z0.real].append((z0, z1))


def on_line_segment(z):
    # is z located on the polygon edge?
    if any(z0.real <= z.real <= z1.real for z0, z1 in dH[z.imag]):
        return True
    if any(z0.imag <= z.imag <= z1.imag for z0, z1 in dV[z.real]):
        return True
    return False


b = 0
while heap:
    neg_A, i, j = heapq.heappop(heap)
    zi = zs[i]
    zj = zs[j]
    zi_ = complex(zi.real, zj.imag)
    zj_ = complex(zj.real, zi.imag)
    hs, vs = hv([zi, zi_, zj, zj_])
    # checking horizontal crossings first gives massive speedup!
    if not crossing(Hs, vs):
        if not crossing(hs, Vs):
            if on_line_segment(zi_) or interior_v(zi_, Hs):
                if on_line_segment(zj_) or interior_v(zj_, Hs):
                    b = -neg_A
                    break
print("answer_b:", b)
