"""
--- Day 11: Space Police ---
https://adventofcode.com/2019/day/11
"""
from aocd import data
from aoc_wim.aoc2019 import IntComputer
from aoc_wim.ocr import AOCR
from collections import deque


class Robot:
    def __init__(self, data, colour0=0):
        self.brain = IntComputer(data, inputs=[colour0])
        self.brain.output = deque(maxlen=2)
        self.position = 0
        self.direction = -1j
        self.painted = {}

    def paint(self):
        while True:
            self.brain.run(until=IntComputer.op_output)
            self.brain.run(until=IntComputer.op_output)
            turn, colour = self.brain.output
            self.painted[self.position] = colour
            self.direction *= [-1j, 1j][turn]
            self.position += self.direction
            self.brain.input.append(self.painted.get(self.position, 0))

    def paint_until_halt(self):
        try:
            self.paint()
        except IntComputer.Halt:
            return


robot = Robot(data)
robot.paint_until_halt()
print("part a:", len(robot.painted))

robot = Robot(data, 1)
robot.paint_until_halt()
rego = AOCR[robot.painted]
print("part b:", rego)
