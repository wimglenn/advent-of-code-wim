"""
--- Day 9: Sensor Boost ---
https://adventofcode.com/2019/day/9
"""
from aocd import data

from aoc_wim.aoc2019 import IntComputer


def compute(data, inputs=()):
    comp = IntComputer(data, inputs=inputs)
    comp.run()
    result = ",".join([str(x) for x in reversed(comp.output)])
    return result


if __name__ == "__main__":
    print("answer_a:", compute(data, inputs=[1]))
    print("answer_b:", compute(data, inputs=[2]))
