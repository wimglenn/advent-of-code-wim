"""
--- Day 13: A Maze of Twisty Little Cubicles ---
https://adventofcode.com/2016/day/13
"""
from aoc_wim.zgrid import ZGrid
from aocd import data


class WallMap:
    def __init__(self, fav_number=None):
        if fav_number is None:
            fav_number = int(data)
        self.fav_number = fav_number

    def __call__(self, z):
        if z.real < 0 or z.imag < 0:
            return "#"
        x, y = z.real, z.imag
        fz = x * x + 3 * x + 2 * x * y + y + y * y
        popcount = bin(int(fz) + self.fav_number).count("1")
        result = "#" if popcount % 2 else "."
        return result


z0 = 1 + 1j
target = 31 + 39j


if __name__ == "__main__":
    grid = ZGrid(WallMap(), on=".", off="#")
    depths = grid.bfs(target=target, z0=z0)
    print("part a:", depths[target])
    depths = grid.bfs(z0=z0, max_depth=50)
    print("part b:", len(depths))
    grid.draw_path(z=target, z0=z0)
