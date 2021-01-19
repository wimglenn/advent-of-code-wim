"""
--- Day 24: Planet of Discord ---
https://adventofcode.com/2019/day/24
"""
from aocd import data
from aoc_wim.zgrid import ZGrid

test_data = """\
....#
#..#.
#..##
..#..
#...."""


def new_empty_grid():
    grid = ZGrid(".....\n" * 5)
    del grid[2 + 2j]
    return grid


def evolve_a(grid):
    d = {}
    for z, g in grid.items():
        n = grid.count_near(z, val="#")
        if g == "#":
            d[z] = ".#"[n == 1]
        elif 1 <= n <= 2:
            d[z] = "#"
        else:
            d[z] = g
    grid.d = d


def part_a(data):
    seen = set()
    grid = ZGrid(data)
    while True:
        k = tuple(grid.items())
        if k in seen:
            return sum(2 ** i for i, glyph in enumerate(grid.values()) if glyph == "#")
        seen.add(k)
        evolve_a(grid)


def evolve_b(grids):
    min_grid = min(grids)
    max_grid = max(grids)
    grids[min_grid - 1] = new_empty_grid()  # add new grid above
    grids[max_grid + 1] = new_empty_grid()  # add new grid below
    new_grids = {}
    for depth, grid in grids.items():
        d = {}
        for z0, glyph in grid.items():
            n = 0
            for z in grid.near(z0):
                if z == 2 + 2j:
                    if depth + 1 not in grids:
                        continue
                    grid_down = grids[depth + 1]
                    if z == z0 + ZGrid.down:
                        n += sum([grid_down[i] == "#" for i in range(5)])
                    elif z == z0 + ZGrid.left:
                        n += sum([grid_down[4 + i * 1j] == "#" for i in range(5)])
                    elif z == z0 + ZGrid.up:
                        n += sum([grid_down[i + 4j] == "#" for i in range(5)])
                    elif z == z0 + ZGrid.right:
                        n += sum([grid_down[i * 1j] == "#" for i in range(5)])
                elif z in grid:
                    n += grid[z] == "#"
                else:
                    if depth - 1 not in grids:
                        continue
                    grid_up = grids[depth - 1]
                    assert z not in grid
                    if z.imag < 0:
                        n += grid_up[2 + 1j] == "#"
                    if z.imag > 4:
                        n += grid_up[2 + 3j] == "#"
                    if z.real < 0:
                        n += grid_up[1 + 2j] == "#"
                    if z.real > 4:
                        n += grid_up[3 + 2j] == "#"
            if glyph == "#":
                if n == 1:
                    d[z0] = "#"
                else:
                    d[z0] = "."
            elif 1 <= n <= 2:
                d[z0] = "#"
            else:
                d[z0] = glyph
        new_grids[depth] = ZGrid(d)
    if "#" not in new_grids[min_grid - 1].values():
        del new_grids[min_grid - 1]
    if "#" not in new_grids[max_grid + 1].values():
        del new_grids[max_grid + 1]
    grids.clear()
    grids.update(new_grids)


def part_b(data, t=200):
    zgrid = ZGrid(data)
    del zgrid[2 + 2j]
    grids = {0: zgrid}
    for i in range(t):
        evolve_b(grids)
    n_bugs = 0
    for depth, grid in sorted(grids.items()):
        # print(f"Depth {depth}:")
        # grid.draw(pretty=False, overlay={2+2j: "?"})
        n_bugs += grid.count("#")
    return n_bugs


if __name__ == "__main__":
    print("part a:", part_a(data))
    print("part b:", part_b(data))
