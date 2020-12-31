"""
--- Day 24: Lobby Layout ---
https://adventofcode.com/2020/day/24
"""
from aocd import data
import re
from aoc_wim import hexgrid


pat = r"(se|sw|ne|nw|e|w)"
grid = hexgrid.HexGrid()
for line in data.splitlines():
    steps = re.findall(pat, line)
    h = sum(getattr(hexgrid, s) for s in steps)
    grid[h] = not grid.get(h, False)
print("part a:", grid.count(True))


for day in range(1, 101):
    h_black = {h for h, v in grid.items() if v}
    tiles_to_visit = h_black.union(*[grid.near(h) for h in h_black])
    tiles_to_update = {}
    for h in tiles_to_visit:
        n_black = grid.count_near(h, val=True)
        if grid.get(h) and n_black == 0 or n_black > 2:
            tiles_to_update[h] = False
        elif n_black == 2:
            tiles_to_update[h] = True
    grid.update(tiles_to_update)
    if day <= 10 or day % 10 == 0:
        print(f"Day {day}:", grid.count(True))
    if day == 10:
        print()
print("part b:", grid.count(True))
