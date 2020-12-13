"""
--- Day 1: No Time for a Taxicab ---
https://adventofcode.com/2016/day/1
"""
from aocd import data
from aoc_wim.zgrid import manhattan_distance


z = 0
dz = -1j
seen = {z}
turns = {"R": 1j, "L": -1j}
b = None
for step in data.split(", "):
    turn, n_blocks = step[0], int(step[1:])
    dz *= turns[turn]
    for block in range(n_blocks):
        z += dz
        if b is None and z in seen:
            b = manhattan_distance(z)
        seen.add(z)

print("part a:", manhattan_distance(z))
print("part b:", b)
