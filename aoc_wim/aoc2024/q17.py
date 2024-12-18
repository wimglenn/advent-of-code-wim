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

quines = []
stack = [[]]
while stack:
    ns = stack.pop()
    for n in range(0o10):
        A = int("".join(map(str, ns + [n])), 8)
        comp.reset(A=A, prog=prog)
        comp.run()
        n_out = len(comp.output)
        if n_out < len(prog):
            if comp.output == prog[-n_out:]:
                if ns or n:
                    stack.append(ns + [n])
        elif comp.output == prog:
            quines.append(A)

print("answer b:", min(quines, default=None))
