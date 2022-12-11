"""
--- Day 10: Cathode-Ray Tube ---
https://adventofcode.com/2022/day/10
"""
from aocd import data
from aoc_wim.ocr import AOCR


lines = iter(data.splitlines())
cycles = {20 + 40*i for i in range(6)}
W, H = 40, 6
crt = {}
x = 1
a = addx = t = 0
for i in range(W * H):
    if i in cycles:
        a += i * x
    if t == 0:
        x += addx
        line = next(lines)
        if line == "noop":
            # model it like an "addx 0" which takes only 1 cycle to complete
            addx, t = 0, 1
        else:
            _op, n = line.split()
            addx, t = int(n), 2
    t -= 1
    row, col = divmod(i, W)
    crt[row, col] = ".#"[abs(col - x) <= 1]


print("part a:", a)
print("part b:", AOCR[crt])
