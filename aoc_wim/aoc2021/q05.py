"""
--- Day 5: Hydrothermal Venture ---
https://adventofcode.com/2021/day/5
"""
from aocd import data
from collections import Counter

da = Counter()
db = Counter()
for line in data.splitlines():
    xy1, xy2 = line.split(" -> ")
    x1, y1 = [int(n) for n in xy1.split(",")]
    x2, y2 = [int(n) for n in xy2.split(",")]
    xstep = 1 if x1 < x2 else -1
    ystep = 1 if y1 < y2 else -1
    xrange = range(x1, x2 + xstep, xstep)
    yrange = range(y1, y2 + ystep, ystep)
    if x1 == x2:  # vertical line
        for y in yrange:
            da[x1, y] += 1
    elif y1 == y2:  # horizontal line
        for x in xrange:
            da[x, y1] += 1
    elif abs(y2 - y1) == abs(x2 - x1):  # diagonal line
        for x, y in zip(xrange, yrange):
            db[x, y] += 1

print("part a:", sum(v > 1 for v in da.values()))
print("part b:", sum(v > 1 for v in (da + db).values()))
