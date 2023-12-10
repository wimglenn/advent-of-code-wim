"""
--- Day 23: Safe Cracking ---
https://adventofcode.com/2016/day/23
"""
from aocd import data

from aoc_wim.aoc2016 import AssembunnyComputer


comp = AssembunnyComputer(data, a0=7)
comp.run()
print("answer_a:", comp.reg["a"])

comp.__init__(data, a0=12)
comp.run()
print("answer_b:", comp.reg["a"])
