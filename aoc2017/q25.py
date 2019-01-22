from aocd import data
from parse import parse
from collections import defaultdict


test_data = """\
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""


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


def parsed(data):
    first, *rest = data.split('\n\n')
    parsed = parse(template_first, first).named
    directions = {'right': 1, 'left': -1}
    for text in rest:
        data = parse(template_rest, text).named
        parsed[data['state_current']] = {
            0: (directions[data['direction0']], data['val0'], data['state0']),
            1: (directions[data['direction1']], data['val1'], data['state1']),
        }
    return parsed


def exe(data):
    prog = parsed(data)
    tape = defaultdict(int)
    cursor = 0
    state = prog['state0']
    for i in range(prog['n']):
        instructions = prog[state]
        val = tape[cursor]
        direction, tape[cursor], state = instructions[val]
        cursor += direction
    return sum(tape.values())


assert exe(test_data) == 3
print("part a:", exe(data))
