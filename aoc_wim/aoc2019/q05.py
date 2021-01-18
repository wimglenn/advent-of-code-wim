"""
--- Day 5: Sunny with a Chance of Asteroids ---
https://adventofcode.com/2019/day/5
"""
from aoc_wim.aoc2019 import IntComputer
from aocd import data


def compute(data, input_val):
    comp = IntComputer(data, inputs=[input_val])
    comp.run()
    result, *zeros = comp.output
    for zero in zeros:
        assert zero == 0
    return result


if __name__ == "__main__":
    print("part a:", compute(data, input_val=1))
    print("part b:", compute(data, input_val=5))
