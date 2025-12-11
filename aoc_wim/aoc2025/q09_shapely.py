"""
--- Day 9: Movie Theater ---
https://adventofcode.com/2025/day/9
"""

from aocd import data
import shapely

xys = [[int(n) for n in xy.split(",")] for xy in data.split()]
P = shapely.Polygon(xys)
shapely.prepare(P)
a = b = 0
for i, (x0, y0) in enumerate(xys):
    for x1, y1 in xys[i + 1 :]:
        area = (abs(x0 - x1) + 1) * (abs(y0 - y1) + 1)
        a = max(a, area)
        p = shapely.Polygon([(x0, y0), (x0, y1), (x1, y1), (x1, y0)])
        if P.contains(p):
            b = max(b, area)
print("answer_a:", a)
print("answer_b:", b)
