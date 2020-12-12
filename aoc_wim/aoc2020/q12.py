"""
--- Day 12: Rain Risk ---
https://adventofcode.com/2020/day/12
"""
from aocd import data
from aoc_wim.zgrid import ZGrid
from aoc_wim.zgrid import manhattan_distance

za = zb = 0
waypoint = 10 - 1j
dz = ZGrid.east

for line in data.splitlines():
    a = line[0]
    n = int(line[1:])
    if a in "NSEW":
        za += n * getattr(ZGrid, a)
        waypoint += n * getattr(ZGrid, a)
    elif a in 'LR':
        n //= 90
        turn = getattr(ZGrid, f"turn{a}")
        dz *= turn ** n
        dw = waypoint - zb
        dw *= turn ** n
        waypoint = zb + dw
    else:
        za += n * dz
        delta = n * (waypoint - zb)
        zb += delta
        waypoint += delta

print("part a:", manhattan_distance(za))
print("part b:", manhattan_distance(zb))
