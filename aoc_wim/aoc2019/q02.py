"""
--- Day 2: 1202 Program Alarm ---
https://adventofcode.com/2019/day/2
"""
from aoc_wim.aoc2019 import IntComputer
from aocd import data


def part_a(data, r1=None, r2=None):
    comp = IntComputer(data)
    if r1 is not None:
        comp.reg[1] = r1
    if r2 is not None:
        comp.reg[2] = r2
    comp.run()
    result = comp.reg[0]
    return result


def part_b(data):
    target = 19690720
    for r1 in range(100):
        for r2 in range(100):
            if part_a(data, r1, r2) == target:
                return 100 * r1 + r2


print(part_a(data, r1=12, r2=2))
print(part_b(data))
