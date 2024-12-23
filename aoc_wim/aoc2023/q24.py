"""
--- Day 24: Never Tell Me The Odds ---
https://adventofcode.com/2023/day/24
"""
from aocd import data
from aocd import extra
from dataclasses import dataclass
import itertools as it
import z3


@dataclass
class Hailstone:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    # TODO: from_line fromline naming consistency
    @classmethod
    def from_line(cls, line):
        return cls(*map(int, line.replace("@", ",").split(",")))


def intersect2d(h0, h1):
    denom = h0.dx * h1.dy - h0.dy * h1.dx
    if denom == 0:
        return float("inf"), float("inf")
    f = h0.y * h0.dx - h0.x * h0.dy
    g = h1.x * h1.dy - h1.y * h1.dx
    px = (f * h1.dx + g * h0.dx) / denom
    py = (f * h1.dy + g * h0.dy) / denom
    return px, py


test_area_min = extra.get("test_area_min", 200_000_000_000_000)
test_area_max = extra.get("test_area_max", 400_000_000_000_000)
a = 0
hailstones = [Hailstone.from_line(line) for line in data.splitlines()]
for h0, h1 in it.combinations(hailstones, 2):
    px, py = intersect2d(h0, h1)
    if test_area_min <= px <= test_area_max and test_area_min <= py <= test_area_max:
        if (px > h0.x and h0.dx > 0) or (px < h0.x and h0.dx < 0):
            if (px > h1.x and h1.dx > 0) or (px < h1.x and h1.dx < 0):
                a += 1
print("answer_a:", a)


x, y, z, dx, dy, dz = z3.Ints("x y z dx dy dz")
ts = z3.Ints("t0 t1 t2")
s = z3.Solver()
for t, h in zip(ts, hailstones):
    s.add(t >= 0)
    s.add(h.x + t * h.dx == x + t * dx)
    s.add(h.y + t * h.dy == y + t * dy)
    s.add(h.z + t * h.dz == z + t * dz)
s.check()
m = s.model()
b = m[x].as_long() + m[y].as_long() + m[z].as_long()
print("answer_b:", b)
