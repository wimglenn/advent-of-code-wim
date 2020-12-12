"""
--- Day 11: Seating System ---
https://adventofcode.com/2020/day/11
"""
from aocd import data
from aoc_wim.zgrid import ZGrid


def evolve(grid, part="a"):
    result = ZGrid(grid.d.copy())
    max_occ = 4 if part == "a" else 5
    for z0, c0 in grid.items():
        if c0 == ".":
            continue  # floor
        if part == "a":
            n_occ = grid.count_near(z0, "#", n=8)
        else:
            n_occ = 0
            for dz in grid.near(0, n=8):
                z = z0
                val = "."
                while val == ".":
                    z += dz
                    val = grid.get(z)
                    n_occ += val == "#"
        if c0 == "L" and n_occ == 0:
            result[z0] = "#"
        if c0 == "#" and n_occ >= max_occ:
            result[z0] = "L"
    return result


for p in "ab":
    grid0 = ZGrid(data)
    while True:
        grid1 = evolve(grid0, part=p)
        grid1.draw(clear=True, pretty=True, transform={".": "  ", "L": "💺", "#": "🧘🏽"})
        if grid1.d == grid0.d:
            break
        grid0 = grid1
    print("part", p, grid0.count("#"))
