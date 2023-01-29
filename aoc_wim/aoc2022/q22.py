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


edges = {
    1: 10,
    2: 9,
    4: 5,
    6: 3,
    7: 8,
    11: 14,
    12: 13,
}
rots = {
    1: 1j,
    2: 1,
    4: 1j,
    6: -1,
    7: 1j,
    11: -1,
    12: 1j,
}
offsets = {
    1: -1+3j,
    2: -2+3j,
    4: -1+1j,
    6: 1-2j,
    7: -1+1j,
    11: 1-2j,
    12: 1-1j,
}
edges.update({v: k for k, v in edges.items()})
offsets.update({edges[k]: -v for k, v in offsets.items()})
rots.update({edges[k]: v.conjugate() for k, v in rots.items()})
dz_Y_edge = {
    (1, 0): 3,
    (1, 1): 5,
    (1, 2): 6,
    (1, 3): 8,
    (-1, 0): 14,
    (-1, 1): 13,
    (-1, 2): 11,
    (-1, 3): 10,
}
dz_X_edge = {
    (1j, 0): 9,
    (1j, 1): 7,
    (1j, 2): 4,
    (-1j, 0): 12,
    (-1j, 1): 1,
    (-1j, 2): 2,
}


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
    44444555
    44445555
    6666
    6666
    6666
    6666
    """
    X, x = divmod(z.real, w)
    Y, y = divmod(z.imag, w)
    if dz in (1, -1):
        edge = dz_Y_edge[dz, Y]
    elif dz in (-1j, 1j):
        edge = dz_X_edge[dz, X]
    z += offsets[edge] * w
    dz *= rots[edge]
    if edge == 2:
        z += (w - 1) * 1j
    elif edge == 9:
        z -= (w - 1) * 1j
    elif edge in (6, 11, 3, 14):
        z = z.real + (z.imag // w) * w * 1j + (w - 1 - y) * 1j
    else:
        z = (z.real // w) * w + (z.imag // w) * w * 1j
        z += y + x * 1j
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
    if (X, Y, dz) == (2, 1, 1):  # 4 -> 6
        z += (1 + 1j) * w - y * (1 + 1j)
        dz = 1j
    elif (X, Y, dz) == (2, 2, 1j):  # 5 -> 2
        z -= (2 + 1j) * w - (w - 1 - x) + x
        dz = -1j
    elif (X, Y, dz) == (1, 1, -1j):  # 3 -> 1
        z -= (1j - 1) * w + (w - 1 - x) * (1 - 1j)
        dz = 1
    return z, dz

    y_ = w - 1 - y
    x_ = w - 1 - x
    match X, Y, dz:
        # case _, 0,   1: return z + (1+2j)*w + y_*1j, -1       # 1 -> 6
        case _, 1,   1: return z + (1+1j)*w - y*(1+1j), 1j    # 4 -> 6
        # case _, 2,   1: return z - (1+2j)*w + y_*1j, -1       # 6 -> 1
        # case _, 0,  -1: return z - (1-1j)*w + y*(1-1j), 1j    # 1 -> 3
        # case _, 1,  -1: return z + (3+1j)*w - y + y_*1j, -1j  # 2 -> 6
        # case _, 2,  -1: return z - (1+1j)*w - y_*(1+1j), -1j  # 5 -> 3
        # case 0, _,  1j: return z + (2+1j)*w + x_-x, -1j       # 2 -> 5
        # case 1, _,  1j: return z + (1+1j)*w - x_*(1+1j), 1    # 3 -> 5
        case 2, _,  1j: return z - (2+1j)*w + x_-x, -1j       # 5 -> 2
        # case 3, _,  1j: return
        # case 0, _, -1j: return
        case 1, _, -1j: return z - (1j-1)*w - x_*(1-1j), 1    # 3 -> 1
        # case 2, _, -1j: return
        # case 3, _, -1j: return


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
        # grid.draw(overlay=path_overlay, empty_glyph=" ")
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
print("part a:", passwd(z, dz))

z, dz = walk_path(z0, dz0, wrap=wrap_b, draw=draw)
print("part b:", passwd(z, dz))
