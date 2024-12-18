"""
--- Day 16: Reindeer Maze ---
https://adventofcode.com/2024/day/16
"""
from aocd import data
from aoc_wim.zgrid import ZGrid
from queue import PriorityQueue
import itertools as it


grid = ZGrid(data, on=".", off="#")
grid.graph(extra="SE")
z0 = grid.z("S")
z1 = grid.z("E")
q = PriorityQueue()
i = it.count()
state = (0, next(i), z0, 1, [])
q.put(state)
while q:
    score, _, z, dz, path = q.get()


# grid = ZGrid(data, on=".", off="#")
# z0 = grid.z("S")
# z1 = grid.z("E")
# grid[z0] = "."
# grid[z1] = "."
# graph = grid.graph()
#
#
# class Q16AStar(AStar):
#     def cost(self, current_state, next_state):
#         result = 1
#         if current_state[1] != next_state[1]:
#             result += 1000
#         return result
#
#     def adjacent(self, state):
#         z0, dz0 = state
#         for z in grid.near(z0):
#             if grid[z] == ".":
#                 yield z, z - z0
#
#     def target_reached(self, current_state, target):
#         return current_state[0] == target[0]
#
#
# astar = Q16AStar((z0, 1), (z1, None))
# paths = astar.run(first=0)
# a = astar.gscore[paths[0][0]]
# print("answer_a:", a)
# b = len({z for path in paths for z, dz in path})
# print("answer_b:", b)
