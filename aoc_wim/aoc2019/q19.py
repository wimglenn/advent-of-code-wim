from aocd import data
from aoc_wim.aoc2019 import IntComputer
from aoc_wim.zgrid import ZGrid
from aoc_wim.search import Bisect
import functools


class OutOfBeam(Exception):
    pass


@functools.lru_cache(maxsize=100**2)
def beam(z):
    comp = IntComputer(data, inputs=[int(z.imag), int(z.real)])
    comp.run(until=IntComputer.op_output)
    [result] = comp.output
    return result


print("populating 50x50 zgrid...")
grid = ZGrid()
x0 = 0
for y in range(50):
    on = False
    for x in range(x0, 50):
        z = x + y*1j
        val = grid[z] = beam(z)
        if not on and val:
            on = True
            x0 = x
            if x0:
                m = y / x0
        if on and not val:
            break
grid.draw()
print("part a", sum(grid.values()))


def left_edge_of_beam(y, gradient):
    x = int(y / gradient)
    z = x + y*1j
    if beam(z):
        while beam(z - 1):
            z -= 1
    else:
        while not beam(z + 1):
            z += 1
        z += 1
    assert beam(z) and not beam(z - 1)
    return z


print("initial gradient is approx -->", m)
print("refining gradient estimate -->", end=" ")
z = left_edge_of_beam(2000, gradient=m)
m = z.imag/z.real
print(m)


def check(y, gradient=m):
    z = left_edge_of_beam(y, gradient)
    val = beam(z + d - d * 1j)
    print(f"y={y}", "wide" if val else "narrow")
    return val


d = 99
bisect = Bisect(check, lo=d)
print("bisecting...")
y = bisect.run() + 1
z = left_edge_of_beam(y, m) - d * 1j
print("part b", int(z.real)*10000 + int(z.imag))
