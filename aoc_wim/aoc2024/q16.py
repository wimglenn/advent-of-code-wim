"""
--- Day 16: Reindeer Maze ---
https://adventofcode.com/2024/day/16
"""
from aocd import data
from aoc_wim.zgrid import ZGrid
from queue import PriorityQueue
import itertools as it


grid = ZGrid(data)
q = PriorityQueue()
i = it.count()
S, E = grid.z("S"), grid.z("E")
state = (0, next(i), S, 1, [S])
q.put(state)
a = None
score = {}
paths = []
while not q.empty():
    s0, _, z0, dz0, path = q.get()
    if s0 > score.get((z0, dz0), float("inf")):
        continue
    score[z0, dz0] = s0
    if z0 == E:
        if a is None:
            a = s0
        if a == s0:
            paths.append(path)
    for z in grid.near(z0):
        if grid[z] == "#":
            continue
        dz = z - z0
        s = s0 + [1001, 1][dz == dz0]
        q.put((s, next(i), z, dz, path + [z]))

print("answer_a:", a)
print("answer_b:", len(set().union(*paths)))
