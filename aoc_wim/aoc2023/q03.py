"""
--- Day 3: Gear Ratios ---
https://adventofcode.com/2023/day/3
"""
from aocd import data
from aoc_wim.zgrid import ZGrid

g = ZGrid(data)
n = []
part = gear = None
part_numbers = []
gears = {}
for z0, glyph in g.scan():
    if glyph.isdigit():
        n.append(glyph)
        for z in g.near(z0, n=8):
            c = g.get(z, ".")
            if not c.isdigit() and c != ".":
                part = True
                if c == "*":
                    gear = z
                    if gear not in gears:
                        gears[gear] = []
        if not g.get(z0 + 1, ".").isdigit():
            if part:
                part_number = int("".join(n))
                part_numbers.append(part_number)
                if gear:
                    gears[gear].append(part_number)
                part = gear = None
            n.clear()

print("answer_a:", sum(part_numbers))
print("answer_b:", sum([g[0] * g[1] for g in gears.values() if len(g) == 2]))
