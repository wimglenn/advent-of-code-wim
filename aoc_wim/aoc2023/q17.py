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
        tail, dz, z0 = state0
        if tail < self.max_tail and z0 + dz in grid:
            yield tail + 1, dz, z0 + dz
        if self.min_tail <= tail:
            for turn in grid.turn_left, grid.turn_right:
                z = z0 + dz * turn
                if z in grid:
                    yield 1, dz * turn, z
        if z0 == 0 and self.min_tail:
            yield 1, 1j, z0 + 1j

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
