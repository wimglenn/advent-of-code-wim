"""
--- Day 23: Opening the Turing Lock ---
https://adventofcode.com/2015/day/23
"""
from aocd import data


class Computer:
    def __init__(self, instructions=""):
        self.reset(instructions=instructions)

    def reset(self, i=0, instructions=""):
        self.i = i
        self.instructions = instructions.strip().splitlines()
        self.registers = {}.fromkeys("ab", 0)

    def compute(self, i=0, verbose=False):
        self.i = i
        while 0 <= self.i < len(self.instructions):
            line = self.instructions[self.i]
            op, args = line.split(None, maxsplit=1)
            args = args.split(", ")
            args = [x if x in self.registers else int(x) for x in args]
            f = getattr(self, op)
            if verbose:
                registers = ["{}:{}".format(k, v) for k, v in self.registers.items()]
                state = ",".join(registers)
                print(state, f"L{i}", op, *args)
            f(*args)
            self.i += 1

    def hlf(self, r):
        self.registers[r] //= 2

    def tpl(self, r):
        self.registers[r] *= 3

    def inc(self, r):
        self.registers[r] += 1

    def jmp(self, offset):
        self.i += offset - 1

    def jie(self, r, offset):
        if self.registers[r] % 2 == 0:
            self.jmp(offset)

    def jio(self, r, offset):
        if self.registers[r] == 1:
            self.jmp(offset)


if __name__ == "__main__":
    computer = Computer()

    computer.reset(instructions=data)
    computer.compute()
    print(computer.registers["b"])

    computer.reset(instructions=data)
    computer.registers["a"] = 1
    computer.compute()
    print(computer.registers["b"])
