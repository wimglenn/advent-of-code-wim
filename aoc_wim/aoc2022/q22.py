"""
--- Day 22: Monkey Map ---
https://adventofcode.com/2022/day/22
"""
import math
import re

from aocd import data

from aoc_wim.zgrid import ZGrid


grid, steps = data.split("\n\n")
grid = ZGrid(grid)
steps = re.split("([LR])", steps)

grid.remove(" ")
dzs = [1, 1j, -1, -1j]
glyph = dict(zip(dzs, ">v<^"))
w = math.isqrt(len(grid) // 6)


def passwd(z, dz):
    return int(1000*(z.imag + 1) + 4*(z.real + 1) + dzs.index(dz))


def wrap_a(z, dz):
    z += dz
    while z - dz in grid:
        z -= w * dz
    return z, dz


def wrap_b_test(z, dz):
    """
            1111
            1111
            1111
            1111
    222233334444
    222233334444
    222233334444
    222233334444
            55556666
            55556666
            55556666
            55556666
    """
    X, x = divmod(z.real, w)
    Y, y = divmod(z.imag, w)
    match dz:
        case 1: return z + (1+1j)*w - y*(1+1j), 1j         # 4 -> 6
        case 1j: return z - (2+1j)*w + w-1-2*x, -1j        # 5 -> 2
        case -1j: return z - (1j-1)*w - (w-1-x)*(1-1j), 1  # 3 -> 1


def wrap_b(z, dz):
    """
        11112222
        11112222
        11112222
        11112222
        3333
        3333
        3333
        3333
    44445555
    44445555
    44445555
    44445555
    6666
    6666
    6666
    6666
    """
    X, x = divmod(z.real, w)
    Y, y = divmod(z.imag, w)
    x_ = w - 1 - x
    y_ = w - 1 - y
    match X, Y, dz:
        case _, 0,  -1: return z - w*(1-2j) + (y_-y)*1j,   1  # 1 -> 4
        case _, 1,  -1: return z - w*(1-1j) + y*(1-1j),   1j  # 3 -> 4
        case _, 2,  -1: return z + w*(1-2j) + (y_-y)*1j,   1  # 4 -> 1
        case _, 3,  -1: return z + w*(1-3j) + y*(1-1j),   1j  # 6 -> 1
        case _, 0,   1: return z - w*(1-2j) + (y_-y)*1j,  -1  # 2 -> 5
        case _, 1,   1: return z + w*(1-1j) - y_*(1-1j), -1j  # 3 -> 2
        case _, 2,   1: return z + w*(1-2j) + (y_-y)*1j,  -1  # 5 -> 2
        case _, 3,   1: return z + w*(1-1j) - y_*(1-1j), -1j  # 6 -> 5
        case 0, _, -1j: return z + w*(1-1j) - x*(1-1j),    1  # 4 -> 3
        case 1, _, -1j: return z - w*(1-3j) - x*(1-1j),    1  # 1 -> 6
        case 2, _, -1j: return z - w*(2-3j) + (w-1)*1j,  -1j  # 2 -> 6
        case 0, _,  1j: return z + w*(2-3j) - (w-1)*1j,   1j  # 6 -> 2
        case 1, _,  1j: return z - w*(1-1j) + x_*(1-1j),  -1  # 5 -> 6
        case 2, _,  1j: return z - w*(1-1j) + x_*(1-1j),  -1  # 2 -> 3


def walk_path(z, dz, wrap, draw=False):
    path_overlay = {z: glyph[dz]}
    for step in steps:
        if step == "R":
            dz *= 1j
        elif step == "L":
            dz *= -1j
        else:
            for _ in range(int(step)):
                z_ = z + dz
                dz_ = dz
                if z_ not in grid:
                    z_, dz_ = wrap(z, dz)
                if grid[z_] == "#":
                    break
                z = z_
                dz = dz_
                path_overlay[z] = glyph[dz]
        path_overlay[z] = glyph[dz]
    if draw:
        grid.draw(overlay=path_overlay, empty_glyph=" ")
    return z, dz


z0 = grid.z(".")
dz0 = 1

draw = False
if w == 4:
    wrap_b = wrap_b_test
    draw = True

z, dz = walk_path(z0, dz0, wrap=wrap_a, draw=draw)
print("answer_a:", passwd(z, dz))

z, dz = walk_path(z0, dz0, wrap=wrap_b, draw=draw)
print("answer_b:", passwd(z, dz))
