from itertools import permutations
from aocd import data
from aoc_wim.aoc2019 import IntComputer


class Amp:
    def __init__(self, data, phase_settings):
        self.comps = [IntComputer(data, inputs=[val]) for val in phase_settings]
        for left, right in zip(self.comps, self.comps[1:] + [self.comps[0]]):
            left.output = right.input

    def run(self):
        self.comps[0].input.appendleft(0)
        while True:
            for comp in self.comps:
                try:
                    comp.run(until=IntComputer.op_output)
                except IntComputer.Halt:
                    return self.comps[-1].output[-1]


def max_thruster_signal(data, part="a"):
    phase = range(5) if part == "a" else range(5, 10)
    return max(Amp(data, p).run() for p in permutations(phase))


tests_a = {
    "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0": 43210,
    "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0": 54321,
    "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0": 65210,
}

tests_b = {
    "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5": 139629729,
    "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10": 18216,
}

for test_data, expected in tests_a.items():
    assert max_thruster_signal(test_data, part="a") == expected

for test_data, expected in tests_b.items():
    assert max_thruster_signal(test_data, part="b") == expected

print(max_thruster_signal(data, part="a"))
print(max_thruster_signal(data, part="b"))
