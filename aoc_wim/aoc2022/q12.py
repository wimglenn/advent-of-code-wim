"""
--- Day 12: Hill Climbing Algorithm ---
https://adventofcode.com/2022/day/12
"""
from aocd import data
from aoc_wim.zgrid import ZGrid
from aoc_wim.search import AStar

grid = ZGrid(data)
start = grid.z("S")
end = grid.z("E")
grid[start] = "a"
grid[end] = "z"


class A𖤐(AStar):
    def adjacent(self, z0):
        return [z for z in grid.near(z0) if ord(grid[z0]) - ord(grid.get(z, "_")) <= 1]

    def target_reached(self, z, target):
        return z == target or grid[z] == target


print("part a:", len(A𖤐(end, start).run()) - 1)
print("part b:", len(A𖤐(end, "a").run()) - 1)
