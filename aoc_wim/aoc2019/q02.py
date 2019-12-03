import logging

from aocd import data


log = logging.getLogger(__name__)


class CatchFire(Exception):
    pass


class IntComputer:
    def __init__(self, reg0):
        self.ip = 0
        self.reg = reg0[:]
        self.op_map = {
            # opcode: (op, jump)
            1: (self.op_add, 4),
            2: (self.op_mul, 4),
            99: (self.op_halt, 1),
        }

    def op_add(self):
        i = self.ip
        A = self.reg
        val = A[A[i + 1]] + A[A[i + 2]]
        A[A[i + 3]] = val

    def op_mul(self):
        i = self.ip
        A = self.reg
        val = A[A[i + 1]] * A[A[i + 2]]
        A[A[i + 3]] = val

    def op_halt(self):
        raise CatchFire

    def step(self):
        opcode = self.reg[self.ip]
        func, jump = self.op_map[opcode]
        func()
        self.ip += jump

    def run(self, n=10 ** 10):
        for i in range(n):
            log.debug("%10d(ip%3d): %s", i, self.ip, self.reg)
            self.step()


def compute(A, noun_verb=None):
    comp = IntComputer(A)
    if noun_verb is not None:
        comp.reg[1:3] = noun_verb
    try:
        comp.run()
    except CatchFire:
        pass
    return comp.reg


def part_a(data, r1=None, r2=None):
    reg = [int(n) for n in data.split(",")]
    if r1 is not None:
        reg[1] = r1
    if r2 is not None:
        reg[2] = r2
    result = compute(reg)
    return result[0]


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
