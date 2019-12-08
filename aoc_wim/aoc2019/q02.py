from aoc_wim.aoc2019 import IntComputer
from aocd import data


def part_a(data, r1=None, r2=None):
    comp = IntComputer(data)
    if r1 is not None:
        comp.reg[1] = r1
    if r2 is not None:
        comp.reg[2] = r2
    comp.run()
    result = comp.reg[0]
    return result


def part_b(data):
    target = 19690720
    for r1 in range(100):
        for r2 in range(100):
            if part_a(data, r1, r2) == target:
                return 100 * r1 + r2


tests = {
    "1,9,10,3,2,3,11,0,99,30,40,50": 3500,
    "1,0,0,0,99": 2,
    "2,3,0,3,99": 2,
    "2,4,4,5,99,0": 2,
    "1,1,1,4,99,5,6,0,99": 30,
}

for code, reg0 in tests.items():
    assert part_a(code) == reg0

print(part_a(data, r1=12, r2=2))
print(part_b(data))
