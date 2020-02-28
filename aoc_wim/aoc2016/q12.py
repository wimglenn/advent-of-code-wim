from aocd import data
from aoc_wim.aoc2016 import AssembunnyComputer


comp = AssembunnyComputer(data)
comp.run()
print("part a:", comp.reg["a"])

comp.__init__(data, c0=1)
comp.run()
print("part b:", comp.reg["a"])
