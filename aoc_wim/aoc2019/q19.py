from aocd import data
from aoc_wim.aoc2019 import IntComputer
from aoc_wim.zgrid import ZGrid, zrange
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


def gradients(grid, d=49):
    bottom_edge = [x + d*1j for x in range(d)]
    right_edge = [d + y*1j for y in reversed(range(d + 1))]
    it = iter(bottom_edge + right_edge)
    for left in it:
        if grid[left]:
            break
    for right in it:
        if not grid[right]:
            break
    m1 = left.imag/left.real
    m2 = right.imag/right.real
    return m1, m2


def refine(m1, m2, x=2000):
    m = (m1 + m2) / 2
    z0 = x + int(m*x)*1j
    if beam(z0) != 1:
        raise OutOfBeam
    left = z0 - 1
    right = z0 + 1
    while beam(left):
        left -= 1
    while beam(right):
        right += 1
    m1 = left.imag/left.real
    m2 = right.imag/right.real
    return m1, m2


def beam_w_h(z):
    if beam(z) != 1:
        raise OutOfBeam
    w = 0
    while True:
        w += 1
        if not beam(z + w):
            break
    h = 0
    while True:
        h += 1
        if not beam(z + h*1j):
            break
    return w, h


def find_in_neighbourhood(z0, r=10, d=100):
    results = []
    for z in zrange(z0 - r - r*1j, z0 + r + r*1j):
        try:
            w, h = beam_w_h(z)
        except OutOfBeam:
            print(z, "--> out")
            continue
        print(z, "-->", (w, h))
        if (w, h) == (d, d):
            results.append(z)
    z = min(results, key=abs)
    print(results)
    result = int(z.real)*10000 + int(z.imag)
    return result


d = 100
m1, m2 = gradients(grid)
m1, m2 = refine(m1, m2)
x = (d + m2*d) / (m1 - m2)
y = m1*x - d
z_approx = int(x) + int(y)*1j
print("part b", find_in_neighbourhood(z_approx, d=d))
