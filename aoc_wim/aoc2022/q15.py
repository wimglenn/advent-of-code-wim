"""
--- Day 15: Beacon Exclusion Zone ---
https://adventofcode.com/2022/day/15
"""
from aocd import data
from parse import parse
from aoc_wim.zgrid import manhattan_distance
from intervaltree import IntervalTree
from itertools import combinations


class Sensor:
    def __init__(self, z, b):
        self.z = z  # sensor position
        self.b = b  # nearest beacon position
        # radius just out of range - i.e. ball perimeter
        self.r = manhattan_distance(z - b) + 1
        # top, right, bottom, left corners of the sensor range
        self.corner = [self.z + self.r * dz for dz in (-1j, 1, 1j, -1)]

    @classmethod
    def fromline(cls, line):
        x1, y1, x2, y2 = parse(template, line).fixed
        return cls(x1 + 1j*y1, x2 + 1j*y2)

    def __contains__(self, z):
        # is the point z detectable from this sensor
        return manhattan_distance(self.z - z) < self.r

    def range_on(self, y):
        # range of x coordinates that are visible at given y coordinate (if any)
        x0, y0 = int(self.z.real), int(self.z.imag)
        r0 = self.r - 1
        dy = abs(y0 - y)
        return range(x0 - r0 + dy, x0 + r0 - dy + 1)


template = "Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}"
sensors = [Sensor.fromline(x) for x in data.splitlines()]

y = 2000000
maxd = 4000000
if len(sensors) == 14:  # example data - smaller bounds are specified in the prose
    y = 10
    maxd = 20

tree = IntervalTree()
for sensor in sensors:
    if xs := sensor.range_on(y):
        tree[xs.start:xs.stop] = 1
tree.merge_overlaps()
a = sum(i.length() for i in tree)
# discount any beacons actually on the line
a -= len({int(s.b.real) for s in sensors if int(s.b.imag) == y})
print("part a:", a)


# the point we're looking for should be just beyond the perimeter of 4 different scanners
# the perimeter in manhattan distance is a diamond shape ◇
# when 4 edges intersect it will look like a rotated #
# we can find intersections of edges like / and \ use as candidates for the search
# when such a point is out of range of *all* the sensors, we have found the solution

def line_intersection(z1, z2, z3, z4):
    # point of intersection of two line segments, specified by 4 complex numbers
    # returns tuple of z_intersection (complex), on_segment1 (bool), on_segment2 (bool)
    z12 = z1 - z2
    z34 = z3 - z4
    if z12 == 0 or z34 == 0:
        raise ValueError("equal start/end points")
    denom = z12.real * z34.imag - z12.imag * z34.real
    if denom == 0:
        raise ValueError("lines are parallel")
    n1 = z1.real * z2.imag - z1.imag * z2.real
    n2 = z3.real * z4.imag - z3.imag * z4.real
    real = (n1 * z34.real - n2 * z12.real) / denom
    imag = (n1 * z34.imag - n2 * z12.imag) / denom
    z = real + 1j * imag
    t = (z1.real - z3.real) * (z3.imag - z4.imag) - (z1.imag - z3.imag) * (z3.real - z4.real)
    u = (z1.real - z3.real) * (z1.imag - z2.imag) - (z1.imag - z3.imag) * (z1.real - z2.real)
    return z, 0 <= t/denom <= 1, 0 <= u/denom <= 1


def tuning_frequency(z):
    return int(z.real) * 4000000 + int(z.imag)


def unique_point_out_of_range():
    for s1, s2 in combinations(sensors, 2):
        for i in range(4):
            z1, z2 = s1.corner[(i + 0) % 4], s1.corner[(i + 1) % 4]
            for j in [0, 2]:
                z3, z4 = s2.corner[(i + j + 1) % 4], s2.corner[(i + j + 2) % 4]
                z, in1, in2 = line_intersection(z1, z2, z3, z4)
                if in1 and in2 and z.real.is_integer() and z.imag.is_integer():
                    if not any(z in s for s in sensors):
                        if 0 <= z.real <= maxd and 0 <= z.imag <= maxd:
                            return z


z = unique_point_out_of_range()
b = tuning_frequency(z)
print("part b:", b)
