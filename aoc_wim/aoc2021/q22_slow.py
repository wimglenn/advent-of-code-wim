"""
--- Day 22: Reactor Reboot ---
https://adventofcode.com/2021/day/22
"""
from aocd import data
from parse import parse
from dataclasses import dataclass


@dataclass
class Cuboid:
    # the non-empty 3D space of {x,y,z} with
    #   x0 <= x < x1
    #   y0 <= y < y1
    #   z0 <= z < z1

    val: str
    x0: int
    x1: int
    y0: int
    y1: int
    z0: int
    z1: int
    small: bool = False

    @classmethod
    def from_line(cls, line):
        template = "{} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}"
        val, x0, x1, y0, y1, z0, z1 = parse(template, line).fixed
        small = all(abs(v) <= 50 for v in (x0, x1, y0, y1, z0, z1))
        return cls(val, x0, x1 + 1, y0, y1 + 1, z0, z1 + 1, small)

    def __contains__(self, other):
        if not isinstance(other, Cuboid):
            return NotImplemented
        return (
            self.x0 <= other.x0 < other.x1 <= self.x1
            and self.y0 <= other.y0 < other.y1 <= self.y1
            and self.z0 <= other.z0 < other.z1 <= self.z1
        )


def total_volume(cuboids):
    xs = sorted(set([c.x0 for c in cuboids] + [c.x1 for c in cuboids]))
    ys = sorted(set([c.y0 for c in cuboids] + [c.y1 for c in cuboids]))
    zs = sorted(set([c.z0 for c in cuboids] + [c.z1 for c in cuboids]))
    result = 0
    for x0, x1 in zip(xs, xs[1:]):
        for y0, y1 in zip(ys, ys[1:]):
            for z0, z1 in zip(zs, zs[1:]):
                cell = Cuboid("", x0, x1, y0, y1, z0, z1)
                for cuboid in reversed(cuboids):
                    if cell in cuboid:
                        if cuboid.val == "on":
                            result += (x1 - x0) * (y1 - y0) * (z1 - z0)
                        break
    return result


cuboids = [Cuboid.from_line(x) for x in data.splitlines()]
small_cuboids = [c for c in cuboids if c.small]

print("part a:", total_volume(small_cuboids))
print("part b:", total_volume(cuboids))
