"""
--- Day 4: Ceres Search ---
https://adventofcode.com/2024/day/4
"""
from aocd import data
from aoc_wim.zgrid import ZGrid; grid = ZGrid(data)


linesT = ["".join(x) for x in zip(*data.splitlines())]

a = 0
for line in data.splitlines():
    a += line.count("XMAS") + line.count("SAMX")
for line in linesT:
    a += line.count("XMAS") + line.count("SAMX")

linesD1 = linesT.copy()
linesD2 = linesT.copy()
for i, line in enumerate(linesT):
    head = " " * i
    tail = " " * (len(line) - 1 - i)
    linesD1[i] = head + line + tail
    linesD2[i] = tail + line + head
linesD1 = ["".join(line) for line in zip(*linesD1)]
linesD2 = ["".join(line) for line in zip(*linesD2)]
for line in linesD1:
    a += line.count("XMAS") + line.count("SAMX")
for line in linesD2:
    a += line.count("XMAS") + line.count("SAMX")

b = 0
for z0, g in grid.items():
    if g == "A":
        vals = "".join([grid.get(z0 + z, ".") for z in [-1j-1, -1j+1, 1j+1, 1j-1]])
        b += vals in ["MSSM", "SSMM", "MMSS", "SMMS"]



print("answer_a:", a)
print("answer_b:", b)
