"""
--- Day 12: Rain Risk ---
https://adventofcode.com/2020/day/12
"""
from aocd import data
from aoc_wim.zgrid import ZGrid
from aoc_wim.zgrid import manhattan_distance

za = zb = 0      # ferry
zw = 10 - 1j     # waypoint
dz = ZGrid.east  # direction

for line in data.splitlines():
    i = line[0]
    n = int(line[1:])
    if i in "NSEW":
        za += n * getattr(ZGrid, i)
        zw += n * getattr(ZGrid, i)
    elif i in "LR":
        n //= 90
        turn = getattr(ZGrid, f"turn{i}")
        dz *= turn ** n
        zw = zb + (zw - zb) * turn ** n
    elif i == "F":
        za += n * dz
        delta = n * (zw - zb)
        zb += delta
        zw += delta

print("part a:", manhattan_distance(za))
print("part b:", manhattan_distance(zb))
