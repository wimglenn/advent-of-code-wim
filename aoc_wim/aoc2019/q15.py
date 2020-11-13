"""
--- Day 15: Oxygen System ---
https://adventofcode.com/2019/day/15
"""
from collections import deque
from aocd import data
from aoc_wim.aoc2019 import IntComputer
from aoc_wim.search import AStar
from aoc_wim.zgrid import ZGrid


NACK = 0
ACK = 1
GOAL = 2


neighbours = {
    -1j: 1,  # NORTH
    +1j: 2,  # SOUTH
    -1: 3,  # WEST
    +1: 4,  # EAST
}


class Q15AStar(AStar):
    def __init__(self, data):
        self.grid = ZGrid({0j: "."})
        self.comp = IntComputer(data)
        self.comp.output = deque(maxlen=1)
        self.freezer = {0j: self.comp.freeze()}
        state0 = 0j
        AStar.__init__(self, state0, None)

    def adjacent(self, z):
        self.comp.unfreeze(self.freezer[z])
        for dz, input_val in neighbours.items():
            self.comp.input.append(input_val)
            self.comp.run(until=IntComputer.op_output)
            [rc] = self.comp.output
            if rc == NACK:
                self.grid[z + dz] = "#"
            else:
                self.grid[z + dz] = "."
                self.freezer[z + dz] = self.comp.freeze()
                back = neighbours[-dz]
                self.comp.input.append(back)
                self.comp.run(until=IntComputer.op_output)
                assert self.comp.output[0]
                if rc == GOAL:
                    self.target = z + dz
                yield z + dz

    def draw(self):
        overlay = {0: "O"}
        if self.target is not None:
            overlay[self.target] = "T"
        self.grid.draw(overlay=overlay)


search = Q15AStar(data)
path = search.run()
print("part a", search.path_length)
search.draw()

s0 = search.freezer[search.target]
search.state0 = search.target
search.target_reached = lambda *args: False
search.comp.unfreeze(s0)
search.fscore.clear()
search.gscore.clear()
search.gscore[search.state0] = 0
search.came_from.clear()
search.closed.clear()
search.run()
print("part b", max(search.gscore.values()))
search.draw()
