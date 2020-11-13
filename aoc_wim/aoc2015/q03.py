"""
--- Day 3: Perfectly Spherical Houses in a Vacuum ---
https://adventofcode.com/2015/day/3
"""
from aocd import data


step = {
    "^": -1j,
    ">": 1,
    "v": 1j,
    "<": -1,
}


z = 0
seen = {z}
for c in data:
    z += step[c]
    seen |= {z}

print("part a:", len(seen))


z = 0
seen = {z}
for c in data[0::2]:  # santa
    z += step[c]
    seen |= {z}

z = 0
for c in data[1::2]:  # robo-santa
    z += step[c]
    seen |= {z}

print("part b:", len(seen))
