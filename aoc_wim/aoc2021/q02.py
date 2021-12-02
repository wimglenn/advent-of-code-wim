"""
--- Day 2: Dive! ---
https://adventofcode.com/2021/day/2
"""
from aocd import data
from aoc_wim.zgrid import ZGrid

aim = za = zb = 0
for line in data.splitlines():
    direction, X = line.split()
    X = int(X)
    dz = ZGrid.dzs[direction] * X
    za += dz
    if direction == "forward":
        zb += dz + aim * X
    else:
        aim += dz

print("part a:", int(za.real) * int(za.imag))
print("part b:", int(zb.real) * int(zb.imag))
