"""
--- Day 17: Chronospatial Computer ---
https://adventofcode.com/2024/day/17
"""
from aocd import data
import re


class Comp:
    combo = {4: "A", 5: "B", 6: "C"}

    def __init__(self, A, B, C, prog=()):
        self.output = []
        self.reset(A, B, C, prog)

    def __getitem__(self, k):
        k = self.combo.get(k, k)
        return self.data.get(k, k)

    def __setitem__(self, k, v):
        k = self.combo.get(k, k)
        self.data[k] = v

    def reset(self, A=0, B=0, C=0, prog=()):
        self.data = {"A": A, "B": B, "C": C}
        self.prog = prog
        self.ip = 0
        self.output.clear()

    def adv(self, x):
        self["A"] >>= self[x]

    def bxl(self, x):
        self["B"] ^= x

    def bst(self, x):
        self["B"] = self[x] & 0o7

    def jnz(self, x):
        if self["A"]:
            self.ip = x - 2

    def bxc(self, x):
        self["B"] ^= self["C"]

    def out(self, x):
        self.output.append(self[x] & 0o7)

    def bdv(self, x):
        self["B"] = self["A"] >> self[x]

    def cdv(self, x):
        self["C"] = self["A"] >> self[x]

    ops = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

    def run(self):
        while self.ip < len(self.prog):
            opcode, operand = self.prog[self.ip:self.ip+2]
            func = self.ops[opcode]
            func(self, operand)
            self.ip += 2
        return ",".join(map(str, self.output))


A, B, C, *prog = map(int, re.findall(r"\d+", data))
comp = Comp(A, B, C, prog=prog)
print("answer_a:", comp.run())

quines = []
stack = [0]
while stack:
    A0 = stack.pop()
    for n in range(0o10):
        A = (A0 << 3) + n
        comp.reset(A=A, prog=prog)
        comp.run()
        if comp.output == prog[-len(comp.output):] and A:
            stack.append(A)
        if comp.output == prog:
            quines.append(A)

print("answer b:", min(quines, default=None))
