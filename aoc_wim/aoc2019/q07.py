"""
--- Day 7: Amplification Circuit ---
https://adventofcode.com/2019/day/7
"""
from itertools import permutations
from aocd import data
from aoc_wim.aoc2019 import IntComputer


class Amp:
    def __init__(self, data, phase_settings):
        self.comps = [IntComputer(data, inputs=[val]) for val in phase_settings]
        for left, right in zip(self.comps, self.comps[1:] + [self.comps[0]]):
            left.output = right.input

    def run(self):
        self.comps[0].input.appendleft(0)
        while True:
            for comp in self.comps:
                try:
                    comp.run(until=IntComputer.op_output)
                except IntComputer.Halt:
                    return self.comps[-1].output[-1]


print("part a:", max(Amp(data, p).run() for p in permutations(range(5))))
print("part b:", max(Amp(data, p).run() for p in permutations(range(5, 10))))
