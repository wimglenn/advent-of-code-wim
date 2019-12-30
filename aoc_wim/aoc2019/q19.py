from aocd import data
from aoc_wim.aoc2019 import IntComputer
from aoc_wim.zgrid import ZGrid, zrange
from collections import deque



d = {}
for z in zrange(50 + 50j):
    comp = IntComputer(data, inputs=[int(z.real), int(z.imag)])
    comp.output = deque(maxlen=1)
    comp.run(until=IntComputer.op_output)
    d[z] = comp.output[0]

g = ZGrid(d)

def v(z):
    comp = IntComputer(data)
    comp.output = deque(maxlen=1)
    comp.input.appendleft(int(z.real))
    comp.input.appendleft(int(z.imag))
    comp.run(until=IntComputer.op_output)
    [val] = comp.output
    d[z] = val
    return val


def wh(z):
    z0 = z
    if v(z) != 1:
        raise Exception
    w = 0
    while True:
        w += 1
        z += 1
        if not v(z):
            break
    z = z0
    h = 0
    while True:
        h += 1
        z += 1j
        if not v(z):
            break
    return w, h


# print(wh(45+19j))  # 3, 6
# z = 45*f+19j*f

x = 424
y = 964
W = 1

for dx in range(-W, W+1):
    for dy in range(-W, W+1):
        z = (x + dx) + (y + dy)*1j
        r = wh(z)
        print(z, "-->", r)
        if r == (100, 100):
            print("boom -> ", int(z.real)*10000 + int(z.imag))
