"""
--- Day 2: I Was Told There Would Be No Math ---
https://adventofcode.com/2015/day/2
"""
from aocd import data


def box_area(w, h, l):
    return 2 * l * w + 2 * w * h + 2 * h * l


def smallest_side(w, h, l):
    return min(l * w, w * h, h * l)


def shortest_perimeter(w, h, l):
    return 2 * min(l + w, w + h, h + l)


def box_volume(w, h, l):
    return w * h * l


area = 0
length = 0
for line in data.splitlines():
    w, h, l = [int(d) for d in line.split("x")]
    area += box_area(w, h, l) + smallest_side(w, h, l)
    length += shortest_perimeter(w, h, l) + box_volume(w, h, l)


print("part a:", area)
print("part b:", length)
