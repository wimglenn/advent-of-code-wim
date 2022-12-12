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
starts = grid.z("a", first=False)


class Q12AStar(AStar):
    def adjacent(self, z0):
        return [z for z in grid.near(z0) if ord(grid.get(z, "⛰")) <= ord(grid[z0]) + 1]


a = len(Q12AStar(start, end).run()) - 1
b = min(len(path) - 1 for s in starts if (path := Q12AStar(s, end).run()) is not None)
print("part a:", a)
print("part b:", b)
