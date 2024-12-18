"""
--- Day 17: Chronospatial Computer ---
https://adventofcode.com/2024/day/17
"""
from aocd import data
from parse import parse


class Comp:
    def __init__(self, A, B=0, C=0, prog=()):
        self.A = A
        self.B = B
        self.C = C
        self.ip = 0
        self.prog = prog
        self.ops = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv,
        ]
        self.output = []

    def reset(self, A=0, B=0, C=0, prog=()):
        self.A = A
        self.B = B
        self.C = C
        self.prog = prog
        self.ip = 0
        self.output.clear()

    def adv(self, x):
        if x == 4:
            x = self.A
        elif x == 5:
            x = self.B
        elif x == 6:
            x = self.C
        self.A >>= x

    def bxl(self, x):
        self.B ^= x

    def bst(self, x):
        if x == 4:
            x = self.A
        elif x == 5:
            x = self.B
        elif x == 6:
            x = self.C
        self.B = x % 8

    def jnz(self, x):
        if self.A:
            self.ip = x - 2

    def bxc(self, x):
        self.B ^= self.C

    def out(self, x):
        if x == 4:
            x = self.A
        elif x == 5:
            x = self.B
        elif x == 6:
            x = self.C
        self.output.append(x % 8)

    def bdv(self, x):
        if x == 4:
            x = self.A
        elif x == 5:
            x = self.B
        elif x == 6:
            x = self.C
        self.B = self.A >> x

    def cdv(self, x):
        if x == 4:
            x = self.A
        elif x == 5:
            x = self.B
        elif x == 6:
            x = self.C
        self.C = self.A >> x

    def run(self):
        while self.ip < len(self.prog):
            opcode = self.prog[self.ip]
            f = self.ops[opcode]
            operand = self.prog[self.ip + 1]
            f(operand)
            self.ip += 2


tdata = """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


template = """\
Register A: {:d}
Register B: 0
Register C: 0

Program: {}"""




A, prog = parse(template, data)
prog = [int(x) for x in prog.split(",")]
comp = Comp(A, prog=prog)
comp.run()
a = ",".join(map(str, comp.output))
print("answer_a:", a)

digits = []
for i, digit in enumerate(reversed(prog)):
    choices = []
    for Ai in range(0o10):
        A = int("".join(map(str, digits + [Ai])), 8)
        comp.reset(A=A, prog=prog)
        comp.run()
        if comp.output[-1] == digit:
            choices.append(A)
    if len(choices) == 1:
        digits.append(choices[0])
    else:
        assert 0

# print(result)

# prog [2, 4, 1, 1, 7, 5, 1, 5, 4, 0, 0, 3, 5, 5, 3, 0]
