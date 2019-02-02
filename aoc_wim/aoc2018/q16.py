from aocd import data
from parse import parse


def all_ops():

    def addr(R, a, b, c):
        R[c] = R[a] + R[b]


    def addi(R, a, b, c):
        R[c] = R[a] + b


    def mulr(R, a, b, c):
        R[c] = R[a] * R[b]


    def muli(R, a, b, c):
        R[c] = R[a] * b


    def banr(R, a, b, c):
        R[c] = R[a] & R[b]


    def bani(R, a, b, c):
        R[c] = R[a] & b


    def borr(R, a, b, c):
        R[c] = R[a] | R[b]


    def bori(R, a, b, c):
        R[c] = R[a] | b


    def setr(R, a, b, c):
        R[c] = R[a]


    def seti(R, a, b, c):
        R[c] = a


    def gtir(R, a, b, c):
        R[c] = int(a > R[b])


    def gtri(R, a, b, c):
        R[c] = int(R[a] > b)


    def gtrr(R, a, b, c):
        R[c] = int(R[a] > R[b])


    def eqir(R, a, b, c):
        R[c] = int(a == R[b])


    def eqri(R, a, b, c):
        R[c] = int(R[a] == b)


    def eqrr(R, a, b, c):
        R[c] = int(R[a] == R[b])

    return locals()


def choices(s):
    ops = all_ops()
    parsed = parse(template, s)
    R0 = list(parsed.fixed[0:4])
    instruction = parsed.fixed[4:8]
    R1 = list(parsed.fixed[8:12])
    choices = []
    for opname, f in ops.items():
        opcode, a, b, c = instruction
        R = R0[:]
        f(R, a, b, c)
        if R == R1:
            choices.append(opname)
    return choices


template = """\
Before: [{:d}, {:d}, {:d}, {:d}]
{:d} {:d} {:d} {:d}
After:  [{:d}, {:d}, {:d}, {:d}]"""


test_data = """\
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]"""


assert len(choices(test_data)) == 3


def part_a(data):
    samples = data.split('\n' * 4)[0].split('\n' * 2)
    result = sum(1 for s in samples if len(choices(s)) >= 3)
    return result


def part_b(data):
    ops = all_ops()
    samples, prog = data.split('\n' * 4)
    samples = samples.split('\n' * 2)
    identified = {}
    while len(identified) < len(ops):
        for s in samples:
            cs = set(choices(s)) - identified.keys()
            if len(cs) == 1:
                [opname] = cs
                opcode = parse(template, s).fixed[4]
                identified[opname] = opcode
    R = [0, 0, 0, 0]
    ops = {opnum: ops[opname] for opname, opnum in identified.items()}
    for line in prog.splitlines():
        opnum, a, b, c = [int(x) for x in line.split()]
        op = ops[opnum]
        op(R, a, b, c)
    return R[0]


if __name__ == "__main__":
    print("part a:", part_a(data))
    print("part b:", part_b(data))
