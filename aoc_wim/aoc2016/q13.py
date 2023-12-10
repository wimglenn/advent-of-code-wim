"""
--- Day 13: A Maze of Twisty Little Cubicles ---
https://adventofcode.com/2016/day/13
"""
from functools import partial

from aocd import data

from aoc_wim.zgrid import ZGrid


def wall(z, fav_number):
    if z.real < 0 or z.imag < 0:
        return "#"
    x, y = z.real, z.imag
    fz = x * x + 3 * x + 2 * x * y + y + y * y
    popcount = bin(int(fz) + fav_number).count("1")
    result = "#" if popcount % 2 else "."
    return result


def make_grid(data):
    func = partial(wall, fav_number=int(data))
    grid = ZGrid(func, on=".", off="#")
    return grid


z0 = 1 + 1j
target = 7 + 4j if data == "10" else 31 + 39j


if __name__ == "__main__":
    grid = make_grid(data)
    depths = grid.bfs(target=target, z0=z0)
    print("answer_a:", depths[target])
    depths = grid.bfs(z0=z0, max_depth=50)
    print("answer_b:", len(depths))
    grid.draw_path(z=target, z0=z0)
