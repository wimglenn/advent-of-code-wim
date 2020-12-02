"""
--- Day 21: Springdroid Adventure ---
https://adventofcode.com/2019/day/21
"""
from aocd import data
from aoc_wim.aoc2019 import IntComputer

# Jump if (there's a hole 1 space away (not A)
#       or there's a hole 2 spaces away (not B)
#       or there's a hole 3 spaces away (not C))
# and there's ground 4 spaces away (D)
prog_a = """\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""

# Jump if (there's a hole 1 space away (not A)
#       or there's a hole 2 spaces away (not B)
#       or there's a hole 3 spaces away (not C))
# and there's ground 4 spaces away (NOT NOT D)
# and (there's ground 8 spaces away (H)
#      or 5 spaces away (E))
prog_b = """\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
NOT D T
NOT T T
AND T J
AND H T
OR E T
AND T J
RUN
"""

for part, prog in zip("ab", [prog_a, prog_b]):
    comp = IntComputer(data, inputs=[ord(x) for x in reversed(prog)])
    comp.run()
    val = comp.output.popleft()
    print(*[chr(x) for x in reversed(comp.output)], sep="")
    print("part", part, val)
