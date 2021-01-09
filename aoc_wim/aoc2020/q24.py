"""
--- Day 24: Lobby Layout ---
https://adventofcode.com/2020/day/24
"""
from aocd import data
import re
from aoc_wim import zgrid


pat = r"(se|sw|ne|nw|e|w)"
grid = zgrid.ZGrid()
for i, line in enumerate(data.splitlines()):
    steps = re.findall(pat, line)
    z = sum([zgrid.hexH[s] for s in steps])
    grid[z] = not grid.get(z)
    # grid.draw_hex(glyph=0, orientation="H", clear=True, title=f" flip {i} ")
print("part a:", grid.count(1))


for day in range(1, 101):
    z_black = {z for z, v in grid.items() if v}
    tiles_to_visit = z_black.union(*[grid.near(z, n=6) for z in z_black])
    tiles_to_update = {}
    for z in tiles_to_visit:
        n_black = grid.count_near(z, n=6, val=1)
        if grid.get(z) and n_black == 0 or n_black > 2:
            tiles_to_update[z] = 0
        elif n_black == 2:
            tiles_to_update[z] = 1
    grid.d.update(tiles_to_update)
    if day <= 10 or day % 10 == 0:
        print(f"Day {day}:", grid.count(1))
    if day == 10:
        print()
print("part b:", grid.count(1))
