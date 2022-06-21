"""
--- Day 22: Reactor Reboot ---
https://adventofcode.com/2021/day/22
"""
from aocd import data
from parse import parse
from dataclasses import dataclass


@dataclass
class Cuboid:
    # 3D space of {x,y,z} with
    #   x0 <= x <= x1
    #   y0 <= y <= y1
    #   z0 <= z <= z1

    x0: int
    x1: int
    y0: int
    y1: int
    z0: int
    z1: int
    val: int

    @classmethod
    def from_line(cls, line):
        template = "{} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}"
        v, x0, x1, y0, y1, z0, z1 = parse(template, line).fixed
        return cls(x0, x1, y0, y1, z0, z1, 1 if v == "on" else -1)

    def __and__(self, other):
        if not isinstance(other, Cuboid):
            return NotImplemented
        x0 = self.x0 if self.x0 > other.x0 else other.x0
        y0 = self.y0 if self.y0 > other.y0 else other.y0
        z0 = self.z0 if self.z0 > other.z0 else other.z0
        x1 = self.x1 if self.x1 < other.x1 else other.x1
        y1 = self.y1 if self.y1 < other.y1 else other.y1
        z1 = self.z1 if self.z1 < other.z1 else other.z1
        if x0 <= x1 and y0 <= y1 and z0 <= z1:
            return Cuboid(x0, x1, y0, y1, z0, z1, -self.val)


def total_volume(cuboids, part="a"):
    if part == "a":
        cuboids = [c for c in cuboids if all(abs(v) <= 50 for v in vars(c).values())]
    cs = []
    for cuboid in cuboids:
        # https://en.wikipedia.org/wiki/Inclusion-exclusion_principle
        extra = [c & cuboid for c in cs]
        cs += [c for c in extra if c is not None]
        if cuboid.val == 1:
            cs.append(cuboid)
    return sum((c.x1 - c.x0 + 1) * (c.y1 - c.y0 + 1) * (c.z1 - c.z0 + 1) * c.val for c in cs)


cuboids = [Cuboid.from_line(x) for x in data.splitlines()]
print("part a:", total_volume(cuboids, part="a"))
print("part b:", total_volume(cuboids, part="b"))
