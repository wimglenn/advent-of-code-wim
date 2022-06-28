"""
--- Day 24: Arithmetic Logic Unit ---
https://adventofcode.com/2021/day/24
"""
from aocd import data
import parse


class Comp:
    def __init__(self, code, inputs):
        self.lines = code.splitlines()
        self.reg = dict.fromkeys("wxyz", 0)
        if isinstance(inputs, int):
            inputs = [int(n) for n in str(inputs)]
        self.input_iter = iter(inputs)

    def inp(self, a):
        self.reg[a] = next(self.input_iter)

    def add(self, a, b):
        try:
            b = int(b)
        except ValueError:
            b = self.reg[b]
        self.reg[a] += b

    def mul(self, a, b):
        try:
            b = int(b)
        except ValueError:
            b = self.reg[b]
        self.reg[a] *= b

    def div(self, a, b):
        try:
            b = int(b)
        except ValueError:
            b = self.reg[b]
        self.reg[a] //= b

    def mod(self, a, b):
        try:
            b = int(b)
        except ValueError:
            b = self.reg[b]
        self.reg[a] %= b

    def eql(self, a, b):
        try:
            b = int(b)
        except ValueError:
            b = self.reg[b]
        self.reg[a] = int(self.reg[a] == b)

    def run(self):
        for i, line in enumerate(self.lines):
            op, *args = line.split()
            f = getattr(self, op)
            f(*args)


optimize = """\
inp w
mul x 0
add x z
mod x 26
div z {:d}
add x {:d}
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y {:d}
mul y x
add z y"""


def solve(data, part="a"):
    div_x_y = [r.fixed for r in parse.findall(optimize, data)]
    if not div_x_y:
        return
    incs = [y for div, x, y in div_x_y if div == 1]
    n_high = int("9" * len(incs))
    n_low = int("1" * len(incs))
    ns = range(n_high, n_low - 1, -1)
    if part == "b":
        ns = reversed(ns)
    for n in ns:
        s_n = str(n)
        if "0" in s_n:
            continue
        it = (int(d) for d in s_n)
        inputs = []
        z = 0
        for div, x, y in div_x_y:
            if div == 1:
                inputs.append(next(it))
                z = 26 * z + inputs[-1] + y
            else:
                i = z % 26 + x
                if not 1 <= i <= 9:
                    break
                inputs.append(i)
                z //= 26
        if z == 0:
            result = sum(10**i * n for i, n in enumerate(reversed(inputs)))
            # verify the result actually works in the VM!
            comp = Comp(code=data, inputs=inputs)
            comp.run()
            assert (
                len(inputs) == 14
                and all(1 <= i <= 9 for i in inputs)
                and comp.reg["z"] == 0
            )
            return result


print("part a:", solve(data, part="a"))
print("part b:", solve(data, part="b"))
