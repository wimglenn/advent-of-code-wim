"""
--- Day 19: A Series of Tubes ---
https://adventofcode.com/2017/day/19
"""
from aocd import data
from aoc_wim.zgrid import ZGrid


grid = ZGrid(data)
z = data.splitlines()[0].index("|")
assert grid[z] == "|"
dz = ZGrid.down
letters = ""
n_steps = 0
while True:
    z += dz
    n_steps += 1
    a = grid.get(z, " ")
    if a == "+":
        dz *= ZGrid.turn_left
        if grid.get(z + dz, " ") == " ":
            dz *= ZGrid.turn_around
    elif a not in "-| ":
        letters += a
    elif a == " ":
        break

print("part a:", letters)
print("part b:", n_steps)
