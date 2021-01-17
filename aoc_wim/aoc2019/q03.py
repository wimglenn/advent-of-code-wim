"""
--- Day 3: Crossed Wires ---
https://adventofcode.com/2019/day/3
"""
from aocd import data
from aoc_wim.zgrid import manhattan_distance
from aoc_wim.zgrid import ZGrid


wires = data.splitlines()
seen = []
for i, wire in enumerate(wires):
    seen.append({})
    z = d = 0
    for step in wire.split(","):
        dz = getattr(ZGrid, step[0])
        for _ in range(int(step[1:])):
            z += dz
            d += 1
            if z not in seen[-1]:
                seen[-1][z] = d

crossings = seen[0].keys() & seen[1].keys()
print("part a:", min([manhattan_distance(z) for z in crossings]))
print("part b:", min([seen[0][z] + seen[1][z] for z in crossings]))
