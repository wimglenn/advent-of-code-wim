"""
--- Day 15: Chiton ---
https://adventofcode.com/2021/day/15
"""
from aocd import data

from aoc_wim.zgrid import ZGrid, manhattan_distance
from aoc_wim.search import AStar
import numpy as np


class Q15AStar(AStar):
    def adjacent(self, state):
        return [z for z in grid.near(state) if z in grid]

    def cost(self, current_state, next_state):
        return grid[next_state]

    def heuristic(self, current_state, next_state):
        return manhattan_distance(current_state, next_state)


grid = ZGrid(data, transform=int)
path = Q15AStar(state0=grid.top_left, target=grid.bottom_right).run()
print("part a:", sum(grid[z] for z in path) - grid[grid.top_left])

A = np.array(grid)  # easier tesselation
A = np.hstack([(A + i) for i in range(5)])
A = np.vstack([(A + i) for i in range(5)])
grid = ZGrid((A - 1) % 9 + 1)

path = Q15AStar(state0=grid.top_left, target=grid.bottom_right).run()
print("part b:", sum(grid[z] for z in path) - grid[grid.top_left])
