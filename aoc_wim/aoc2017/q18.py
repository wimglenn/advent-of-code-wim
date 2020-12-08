"""
--- Day 18: Duet ---
https://adventofcode.com/2017/day/18
"""
from aocd import data
from collections import deque
from aoc_wim.aoc2017 import Comp

# import logging; logging.basicConfig(format="%(message)s", level=logging.DEBUG)

comp = Comp(data, ch_rcv=deque([""]))
while comp.ch_rcv and not comp.blocked():
    comp.step()
print("part a:", comp.ch_snd[-1])

comp0 = Comp(data, pid=0)
comp1 = Comp(data, pid=1)
comp0.ch_snd = comp1.ch_rcv
comp1.ch_snd = comp0.ch_rcv
while not (comp0.blocked() and comp1.blocked()):
    if not comp0.blocked():
        comp0.step()
    if not comp1.blocked():
        comp1.step()
print("part b:", comp1.n_snd)
