from aocd import data
from aoc_wim.aoc2019 import IntComputer
from aoc_wim.zgrid import ZGrid, zrange
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


grid = ZGrid({z: beam(z) for z in zrange(50 + 50j)})
print("part a", sum(grid.values()))


def gradient(grid, d=49):
    # gradient of the left edge of the tractor beam
    bottom_edge = [x + d*1j for x in range(d)]
    right_edge = [d + y*1j for y in reversed(range(d + 1))]
    z = next(z for z in bottom_edge + right_edge if grid[z])
    grad = z.imag/z.real
    return grad


def find_left_edge_of_beam(y, gradient):
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


print("estimating gradient...")
m = gradient(grid)
print("gradient -->", m)
print("refining estimate...")
z = find_left_edge_of_beam(y=2000, gradient=m)
m = z.imag/z.real
print("gradient -->", m)


def check(row, gradient=m):
    z = find_left_edge_of_beam(row, gradient)
    val = beam(z + d - d * 1j)
    print(f"y={row}", "wide" if val else "narrow")
    return val


d = 99
bisect = Bisect(check, lo=d)
print("bisecting...")
row = bisect.run() + 1
z = find_left_edge_of_beam(row, m) - d * 1j
print("part b", int(z.real)*10000 + int(z.imag))
