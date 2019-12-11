from aocd import data
from aoc_wim.aoc2019 import IntComputer
from aoc_wim.ocr import AOCR
from collections import defaultdict


class Robot:
    def __init__(self, data):
        self.brain = IntComputer(data)
        self.position = 0j
        self.direction = 1j
        self.painted = defaultdict(int)

    def paint(self, colour0):
        self.brain.input.append(colour0)
        while True:
            self.brain.run(until=IntComputer.op_output)
            self.brain.run(until=IntComputer.op_output)
            turn, colour = self.brain.output
            self.painted[self.position] = colour
            self.direction *= [1j, -1j][turn]
            self.position += self.direction
            self.brain.output.clear()
            self.brain.input.append(self.painted[self.position])

    def paint_until_halt(self, colour0):
        try:
            self.paint(colour0=colour0)
        except IntComputer.Halt:
            return


def part_a(data):
    robot = Robot(data)
    robot.paint_until_halt(colour0=0)
    n_panels = len(robot.painted)
    return n_panels


def part_b(data):
    robot = Robot(data)
    robot.paint_until_halt(colour0=1)
    rego = AOCR[robot.painted]
    return rego


print(part_a(data))
print(part_b(data))
