"""
--- Day 13: Care Package ---
https://adventofcode.com/2019/day/13
"""
from collections import deque
from aocd import data
from aoc_wim.aoc2019 import IntComputer


class Game:
    def __init__(self, data):
        self.cpu = IntComputer(data)
        self.cpu.input = self
        self.cpu.output = deque(maxlen=3)
        self.paddle_position = 0
        self.ball_position = 0
        self.n_blocks = 0
        self.score = 0

    def pop(self):
        p = self.paddle_position
        b = self.ball_position
        return -1 if b < p else 0 if b == p else 1

    def step(self):
        self.cpu.run(until=IntComputer.op_output)
        self.cpu.run(until=IntComputer.op_output)
        self.cpu.run(until=IntComputer.op_output)
        val, y, x = self.cpu.output
        if val == 2:
            self.n_blocks += 1
        elif val == 3:
            self.paddle_position = x
        elif val == 4:
            self.ball_position = x
        if x == -1 and y == 0:
            self.score = val

    def play(self):
        while True:
            try:
                self.step()
            except IntComputer.Halt:
                return


game_a = Game(data)
game_a.play()
print("part a:", game_a.n_blocks)

game_b = Game(data)
game_b.cpu.reg[0] = 2
game_b.play()
print("part b:", game_b.score)
