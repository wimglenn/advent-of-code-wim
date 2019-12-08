from aoc_wim.aoc2019 import IntComputer
from aocd import data


def compute(data, input_val):
    comp = IntComputer(data, inputs=[input_val])
    comp.run()
    result, *zeros = comp.output
    for zero in zeros:
        assert zero == 0
    return result


assert compute("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", input_val=0) == 0
assert compute("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", input_val=1) == 1
assert compute("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", input_val=7) == 1
assert compute("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", input_val=-3) == 1
assert compute("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", input_val=0) == 0
assert compute("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", input_val=1) == 1
assert compute("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", input_val=42) == 1
assert compute("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", input_val=-123) == 1

test_prog = (
    "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
    "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,"
    "1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
)
assert compute(test_prog, input_val=3) == 999
assert compute(test_prog, input_val=8) == 1000
assert compute(test_prog, input_val=123) == 1001

print(compute(data, input_val=1))
print(compute(data, input_val=5))
