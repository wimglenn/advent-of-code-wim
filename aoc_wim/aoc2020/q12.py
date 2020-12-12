"""
--- Day 12: Rain Risk ---
https://adventofcode.com/2020/day/12
"""
from aocd import data
from aoc_wim.zgrid import ZGrid
from aoc_wim.zgrid import manhattan_distance

za = zb = 0                          # ferry
dza = ZGrid.east                     # direction (part a)
dzb = 10 * ZGrid.east + ZGrid.north  # velocity (part b)

for line in data.splitlines():
    i = line[0]
    n = int(line[1:])
    if i in "NSEW":
        za += n * getattr(ZGrid, i)
        dzb += n * getattr(ZGrid, i)
    elif i in "LR":
        n //= 90
        turn = getattr(ZGrid, f"turn{i}")
        dza *= turn ** n
        dzb *= turn ** n
    elif i == "F":
        za += n * dza
        zb += n * dzb

print("part a:", manhattan_distance(za))
print("part b:", manhattan_distance(zb))
