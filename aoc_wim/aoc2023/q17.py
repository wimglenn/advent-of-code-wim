"""
--- Day 17: Clumsy Crucible ---
https://adventofcode.com/2023/day/17
"""
from aocd import data

from aoc_wim.search import AStar
from aoc_wim.zgrid import ZGrid


class Q17AStar(AStar):
    def __init__(self, state0, min_tail, max_tail):
        self.min_tail = min_tail
        self.max_tail = max_tail
        super().__init__(state0, None)

    def cost(self, current_state, next_state):
        return grid[next_state[-1]]

    def adjacent(self, state0):
        tail, dz, z = state0
        adj = []
        if tail < self.max_tail and z + dz in grid:
            adj.append((tail + 1, dz, z+dz))
        if self.min_tail <= tail and z + dz * 1j in grid:
            adj.append((1, dz * 1j, z + dz * 1j,))
        if self.min_tail <= tail and z + dz * -1j in grid:
            adj.append((1, dz * -1j, z + dz * -1j,))
        if z == 0 and self.min_tail:
            adj.append((1, 1j, z + 1j))
        return adj

    def target_reached(self, current_state, target):
        tail, dz, z = current_state
        return z == bottom_right and tail >= self.min_tail


grid = ZGrid(data, transform=int)
s0 = (0, 1, 0)  # state vector: tail-length, direction, position
bottom_right = grid.bottom_right  # target

astar = Q17AStar(s0, min_tail=0, max_tail=3)
astar.run()
print("answer_a:", astar.gscore[astar.target])

bstar = Q17AStar(s0, min_tail=4, max_tail=10)
bstar.run()
print("answer_b:", bstar.gscore[bstar.target])
