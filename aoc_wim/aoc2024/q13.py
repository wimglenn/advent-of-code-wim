"""
--- Day 13: Claw Contraption ---
https://adventofcode.com/2024/day/13
"""
from aocd import data
import parse

template = """\
Button A: X+{:d}, Y+{:d}
Button B: X+{:d}, Y+{:d}
Prize: X={:d}, Y={:d}"""
ab = [0, 0]
for game in parse.findall(template, data):
    ax, ay, bx, by, X, Y = game.fixed
    denom = ax * by - bx * ay
    for o in 0, 10**13:
        pa, ra = divmod(by * (X + o) - bx * (Y + o), denom)
        pb, rb = divmod(ax * (Y + o) - ay * (X + o), denom)
        if not ra and not rb:
            ab[o > 0] += 3 * pa + pb
a, b = ab

print("answer_a:", a)
print("answer_b:", b)
