"""
--- Day 19: Tractor Beam ---
https://adventofcode.com/2019/day/19
"""
from aocd import data
from aoc_wim.aoc2019 import IntComputer
from aoc_wim.zgrid import ZGrid
from aoc_wim.search import Bisect
import functools


@functools.lru_cache(maxsize=100**2)
def beam(z):
    comp = IntComputer(data, inputs=[int(z.imag), int(z.real)])
    comp.run(until=IntComputer.op_output)
    [result] = comp.output
    return result


def left_edge_of_beam(y, gradient, beam=beam):
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


def locate_square(beam, width, gradient_estimate=1., hi=None):
    d = width - 1

    def check(y):
        z = left_edge_of_beam(y, gradient_estimate, beam)
        val = beam(z + d * ZGrid.NE)
        print(f"y={y}", "wide" if val else "narrow")
        return val

    bisect = Bisect(check, lo=d, hi=hi)
    print("bisecting...")
    y = bisect.run() + 1
    z = left_edge_of_beam(y, gradient_estimate, beam) + d * ZGrid.N
    return z


if __name__ == "__main__":
    print("populating 50x50 zgrid...")
    grid = ZGrid()
    x0 = 0
    for y in range(50):
        on = False
        for x in range(x0, 50):
            z = x + y * 1j
            val = grid[z] = beam(z)
            if not on and val:
                on = True
                x0 = x
                if x0:
                    m = y / x0
            if on and not val:
                break

    print("part a", sum(grid.values()))
    grid.translate({0: ".", 1: "#"})
    grid.draw()

    print("initial gradient is approx -->", m)
    print("refining gradient estimate -->", end=" ")
    z = left_edge_of_beam(2000, gradient=m)
    m = z.imag/z.real
    print(m)

    z = locate_square(beam, width=100, gradient_estimate=m)
    print("part b", int(z.real)*10000 + int(z.imag))
