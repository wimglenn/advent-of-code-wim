"""
--- Day 25: The Halting Problem ---
https://adventofcode.com/2017/day/25
"""
from collections import defaultdict

from aocd import data
from parse import parse


template_first = """\
Begin in state {state0}.
Perform a diagnostic checksum after {n:d} steps."""


template_rest = """\
In state {state_current}:
  If the current value is 0:
    - Write the value {val0:d}.
    - Move one slot to the {direction0}.
    - Continue with state {state0}.
  If the current value is 1:
    - Write the value {val1:d}.
    - Move one slot to the {direction1}.
    - Continue with state {state1}."""


first, *rest = data.split("\n\n")
prog = parse(template_first, first).named
directions = {"right": 1, "left": -1}
for text in rest:
    data = parse(template_rest, text).named
    prog[data["state_current"]] = {
        0: (directions[data["direction0"]], data["val0"], data["state0"]),
        1: (directions[data["direction1"]], data["val1"], data["state1"]),
    }

tape = defaultdict(int)
cursor = 0
state = prog["state0"]
for i in range(prog["n"]):
    instructions = prog[state]
    val = tape[cursor]
    direction, tape[cursor], state = instructions[val]
    cursor += direction

print(sum(tape.values()))
