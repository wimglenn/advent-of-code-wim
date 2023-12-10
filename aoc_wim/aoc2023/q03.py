"""
--- Day 3: Gear Ratios ---
https://adventofcode.com/2023/day/3
"""
from aocd import data

from aoc_wim.zgrid import ZGrid

g = ZGrid(data)
n = []
part = None
part_numbers = []
gear = []
gears = {z: [] for z in g.z("*", first=False)}
for z0, glyph in g.scan():
    if glyph.isdigit():
        n.append(glyph)
        for z in g.near(z0, n=8):
            c = g.get(z, ".")
            if not c.isdigit() and c != ".":
                part = True
                if c == "*":
                    gear.append(z)
        if not g.get(z0 + 1, ".").isdigit():
            if part:
                part_number = int("".join(n))
                part_numbers.append(part_number)
                if gear:
                    for z in set(gear):
                        gears[z].append(part_number)
                part = None
                gear.clear()
            n.clear()

print("answer_a:", sum(part_numbers))
print("answer_b:", sum([g[0] * g[1] for g in gears.values() if len(g) == 2]))
