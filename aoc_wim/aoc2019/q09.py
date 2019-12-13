from aocd import data
from aoc_wim.aoc2019 import IntComputer


def compute(data, inputs=()):
    comp = IntComputer(data, inputs=inputs)
    comp.run()
    result = ",".join([str(x) for x in reversed(comp.output)])
    return result


quine = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
tests = {
    quine: quine,
    "1102,34915192,34915192,7,4,7,99,0": "1219070632396864",
    "104,1125899906842624,99": "1125899906842624",
}
for input_data, expected_output in tests.items():
    assert compute(input_data) == expected_output

print(compute(data, inputs=[1]))
print(compute(data, inputs=[2]))
