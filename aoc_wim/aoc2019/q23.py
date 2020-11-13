"""
--- Day 23: Category Six ---
https://adventofcode.com/2019/day/23
"""
import logging
from aocd import data
from aoc_wim.aoc2019 import IntComputer


log = logging.getLogger(__name__)


class Network:
    def __init__(self, data):
        self.y0 = set()
        self.xy = None, None
        self.comps = [IntComputer(data, inputs=[i]) for i in range(50)]
        self.done = False

    def step(self):
        for i, comp in enumerate(self.comps):
            try:
                comp.run(until=IntComputer.op_output)
            except IndexError:
                # attempted pop from an empty deque
                comp.input.appendleft(-1)
                comp.step()
            if len(comp.output) >= 3:
                # 3 outputs: packet ready to consume/transmit
                dest = comp.output.pop()
                x = comp.output.pop()
                y = comp.output.pop()
                log.info("comp[%d] sends (x=%d, y=%d) to comp[%d]", i, x, y, dest)
                if dest == 0xFF:
                    self.xy = x, y
                    if any(c.output or c.input for c in self.comps):
                        continue
                    if not self.y0:
                        print("part a", y)
                    if y in self.y0:
                        print("part b", y)
                        nic.done = True
                    dest = 0
                    self.y0.add(y)
                self.comps[dest].input.appendleft(x)
                self.comps[dest].input.appendleft(y)

    def run(self):
        while not self.done:
            nic.step()


nic = Network(data)
nic.run()
