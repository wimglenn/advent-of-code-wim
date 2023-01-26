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


def passwd(z, dz):
    return int(1000*(z.imag + 1) + 4*(z.real + 1) + dzs.index(dz))


def warp_a(z, dz):
    while z in grid:
        z -= dz
    return z + dz, dz


w = math.isqrt(len(grid) // 6)
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


def warp_b(z, dz):
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


def walk_path(z, dz, warp, draw=False):
    path_overlay = {z: glyph[dz]}
    for step in steps:
        if step == "R":
            dz *= 1j
        elif step == "L":
            dz *= -1j
        else:
            for _ in range(int(step)):
                n_ = z + dz
                dz_ = dz
                if n_ not in grid:
                    n_, dz_ = warp(z, dz)
                if grid[n_] == ".":
                    z = n_
                    dz = dz_
                    path_overlay[z] = glyph[dz]
        path_overlay[z] = glyph[dz]
    if draw:
        grid.draw(overlay=path_overlay, empty_glyph=" ")
    return z, dz


z0 = grid.z(".")
dz0 = 1

z, dz = walk_path(z0, dz0, warp=warp_a)
print("part a:", passwd(z, dz))

z, dz = walk_path(z0, dz0, warp=warp_b)
print("part b:", passwd(z, dz))
