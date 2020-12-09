"""
--- Day 8: Handheld Halting ---
https://adventofcode.com/2020/day/8
"""
from aocd import data
from aoc_wim.aoc2020 import Comp

# import logging; logging.basicConfig(format="%(message)s", level=logging.DEBUG)

ops = []
for line in data.splitlines():
    op, arg = line.split()
    ops.append((op, int(arg)))

comp = Comp(ops)
seen = {comp.line: comp.a}
while True:
    comp.step()
    if comp.line in seen:
        break
    seen[comp.line] = comp.a
print("part a:", comp.a)

comps = []
flipper = {"nop": "jmp", "jmp": "nop"}
for i, (op, arg) in enumerate(ops):
    if op in flipper:
        c_ops = ops[:]
        c_ops[i] = (flipper[op], arg)
        comp = Comp(c_ops)
        comps.append(comp)

done = False
while not done:
    for comp in comps:
        comp.step()
        if comp.line == len(ops):
            done = True
            break
print("part b:", comp.a)
