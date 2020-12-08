"""
--- Day 23: Coprocessor Conflagration ---
https://adventofcode.com/2017/day/23
"""
from aocd import data
from aoc_wim.aoc2017 import Comp

# import logging; logging.basicConfig(format="%(message)s", level=logging.DEBUG)

comp_a = Comp(data)
while not comp_a.blocked():
    comp_a.step()
print("part a:", comp_a.n_mul)

comp_b = Comp(data, a0=1)
comp_b.code[8:10] = ("wtf", "f", "b"), ("jnz", "1", "15")
while not comp_b.blocked():
    comp_b.step()
print("part b:", comp_b.reg["h"])
