from aoc_wim.aoc2019 import IntComputer
from aocd import data
import random


def compute(data, input_val):
    comp = IntComputer(data, inputs=[input_val])
    comp.run()
    result, *zeros = comp.output
    for zero in zeros:
        assert zero == 0
    return result


test_progs = {
    "eq8_pos": "3,9,8,9,10,9,4,9,99,-1,8",
    "lt8_pos": "3,9,7,9,10,9,4,9,99,-1,8",
    "eq8_imm": "3,3,1108,-1,8,3,4,3,99",
    "lt8_imm": "3,3,1107,-1,8,3,4,3,99",
    "ne0_pos": "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9",
    "ne0_imm": "3,3,1105,-1,9,1101,0,0,12,4,12,99,1",
    "cmp8": (
        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
        "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,"
        "1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    ),
}

assert compute(test_progs["eq8_pos"], input_val=8) == 1
assert compute(test_progs["eq8_imm"], input_val=8) == 1
assert compute(test_progs["lt8_pos"], input_val=8) == 0
assert compute(test_progs["lt8_imm"], input_val=8) == 0
assert compute(test_progs["cmp8"], input_val=8) == 1000
for _ in range(50):
    lt8 = random.randint(-100, 7)
    gt8 = random.randint(9, 100)
    assert compute(test_progs["eq8_pos"], input_val=lt8) == 0
    assert compute(test_progs["eq8_imm"], input_val=lt8) == 0
    assert compute(test_progs["lt8_pos"], input_val=lt8) == 1
    assert compute(test_progs["lt8_imm"], input_val=lt8) == 1
    assert compute(test_progs["eq8_pos"], input_val=gt8) == 0
    assert compute(test_progs["eq8_imm"], input_val=gt8) == 0
    assert compute(test_progs["lt8_pos"], input_val=gt8) == 0
    assert compute(test_progs["lt8_imm"], input_val=gt8) == 0
    assert compute(test_progs["cmp8"], input_val=lt8) == 999
    assert compute(test_progs["cmp8"], input_val=gt8) == 1001

assert compute(test_progs["ne0_pos"], input_val=0) == 0
assert compute(test_progs["ne0_imm"], input_val=0) == 0
for _ in range(50):
    ne0 = random.randint(1, 100)
    assert compute(test_progs["ne0_pos"], input_val=ne0) == 1
    assert compute(test_progs["ne0_imm"], input_val=ne0) == 1

print(compute(data, input_val=1))
print(compute(data, input_val=5))
