"""
--- Day 17: Trick Shot ---
https://adventofcode.com/2021/day/17
"""
from aocd import data
from parse import parse
from aoc_wim.zgrid import ZGrid


def launch(dx, dy, draw=False):
    x = y = y_max = 0
    xys = []
    while y >= y0 and x <= x1:
        x += dx
        y += dy
        xys.append((x, y))
        dx -= 1 if dx > 0 else -1 if dx < 0 else 0  # drag
        dy -= 1  # gravity
        y_max = max(y_max, y)
        if (x, y) in target_area:
            if draw:
                grid = ZGrid({0: "S"} | {complex(*z): "T" for z in target_area})
                grid.draw(flip="y", overlay={complex(*xy): "#" for xy in xys})
            return y_max


x0, x1, y0, y1 = parse("target area: x={:d}..{:d}, y={:d}..{:d}", data).fixed
target_area = {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
dx_min = 1
while sum(range(dx_min + 1)) < x0:  # while target area is undershot horizontally
    dx_min += 1   # anything less is too slow to reach the target horizontally
dx_max = x1 + 1   # anything more overshooting horizontally on the first iteration
dy_min = y0 - 1   # anything less undershooting vertically on the first iteration
dy_max = 1 - y0   # anything higher is coming down too hot

a = b = 0
for dx in range(dx_min, dx_max + 1):
    for dy in range(dy_min, dy_max + 1):
        y = launch(dx, dy)
        if y is not None:
            b += 1
            if y > a:
                a = y
                dxy_best = dx, dy

print("part a:", a)
print("part b:", b)
