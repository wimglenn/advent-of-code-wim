"""
--- Day 15: Chiton ---
https://adventofcode.com/2021/day/15
"""
from aocd import data

from aoc_wim import zgrid
from aoc_wim.search import AStar


class Q15AStar(AStar):
    def adjacent(self, state):
        return [z for z in grid.near(state) if z in grid]

    def cost(self, current_state, next_state):
        return grid[next_state]

    def heuristic(self, current_state, next_state):
        return zgrid.manhattan_distance(current_state, next_state)


grid = zgrid.ZGrid(data, transform=int)
path = Q15AStar(state0=grid.top_left, target=grid.bottom_right).run()
print("part a:", sum(grid[z] for z in path) - grid[grid.top_left])

h, w = grid.height, grid.width
for z in zgrid.zrange(5 * (grid.bottom_right + 1 + 1j)):
    qr, rr = divmod(z.real, w)
    qi, ri = divmod(z.imag, h)
    grid[z] = (grid[complex(rr, ri)] + int(qr) + int(qi) - 1) % 9 + 1

path = Q15AStar(state0=grid.top_left, target=grid.bottom_right).run()
print("part b:", sum(grid[z] for z in path) - grid[grid.top_left])
