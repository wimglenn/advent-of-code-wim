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


class AStarA(AStar):
    def adjacent(self, z0):
        return [z for z in grid.near(z0) if ord(grid.get(z, "‾")) - ord(grid[z0]) <= 1]


class AStarB(AStar):
    def adjacent(self, z0):
        return [z for z in grid.near(z0) if ord(grid.get(z, "_")) - ord(grid[z0]) >= -1]

    def target_reached(self, z, target):
        return grid[z] == target


print("part a:", len(AStarA(start, end).run()) - 1)
print("part b:", len(AStarB(end, "a").run()) - 1)
