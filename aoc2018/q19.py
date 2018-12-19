from aocd import data
import math


test_data = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""


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


def parsed(data):
    lines = data.splitlines()
    ip = int(lines.pop(0).split()[1])
    lines = [s.split() for s in lines]
    lines = [[a, int(b), int(c), int(d)] for a,b,c,d in lines]
    return ip, lines


funcs = all_ops()


class Comp:

    dbg = True

    def __init__(self, ip, d, r0, hacked):
        self.hacked = hacked
        self.ip = ip
        self.i = 0
        self.d = d
        self.r = [0]*6
        self.r[0] = r0

    def step(self):
        opname, a, b, c = self.d[self.i]
        op = funcs[opname]
        self.r[self.ip] = self.i
        op(self.r, a, b, c)
        self.r[self.ip] += 1
        self.i = self.r[self.ip]
        if self.hacked and self.i == 1:
            self.r[0] = sum(divisors(self.r[-1]))
            [][0]


def run(data, r0=0, hack=False):
    ip, lines = parsed(data)
    comp = Comp(ip, lines, r0=r0, hacked=hack)
    while True:
        try:
            comp.step()
        except IndexError:
            break
    return comp.r[0]


def divisors(n):
    divs = [1, n]
    for i in range(2, int(math.sqrt(n)) + 1):
        if not n % i:
            divs.extend([i, n//i])
    return sorted(set(divs))


assert run(test_data) == 7

a = run(data, r0=0, hack=True)
print(a)  # 1152

b = run(data, r0=1, hack=True)
print(b)  # 12690000
