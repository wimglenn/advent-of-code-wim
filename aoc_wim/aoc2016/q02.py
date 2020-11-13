"""
--- Day 2: Bathroom Security ---
https://adventofcode.com/2016/day/2
"""
from aocd import data
from aoc_wim.zgrid import ZGrid


keypad_a = """\
123
456
789
"""


keypad_b = """\
  1
 234
56789
 ABC
  D
"""


def decode(keypad):
    keypad = ZGrid(keypad)
    z = keypad.z("5")
    code = ""
    for line in data.splitlines():
        for direction in line:
            dz = getattr(ZGrid, direction)
            if keypad.get(z + dz, " ").strip():
                z += dz
        code += keypad[z]
    return code


print("part a:", decode(keypad_a))
print("part b:", decode(keypad_b))
