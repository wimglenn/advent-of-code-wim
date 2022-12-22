"""
--- Day 22: Monkey Map ---
https://adventofcode.com/2022/day/22
"""
from aocd import data
from aoc_wim.zgrid import ZGrid

g, path = data.split("\n\n")
distances = [int(n) for n in path.replace("L", "R").split("R")]
turns = "".join(x for x in path if not x.isdigit())
steps = [s for tup in zip(*[distances, turns]) for s in tup] + [distances[-1]]
grid = ZGrid(g, off=" ")

z0 = grid.z(".")
dz0 = 1


facing = [1, 1j, -1, -1j]


def passwd(z, dz):
    return int(1000*(z.imag+1) + 4*(z.real+1) + facing.index(dz))


glyph = dict(zip(facing, ">v<^"))
path_overlay = {z0: glyph[dz0]}
z = grid.z(".")
dz = 1
for step in steps:
    if step == "R":
        dz *= 1j
    elif step == "L":
        dz *= -1j
    else:
        assert isinstance(step, int)
        for _ in range(step):
            next_z = z + dz
            if grid.get(next_z, " ") == " ":
                next_z = z
                while grid.get(next_z, " ") != " ":
                    next_z -= dz
                next_z += dz
            assert next_z in grid
            if grid[next_z] == "#":
                break
            z = next_z
            path_overlay[z] = glyph[dz]
    path_overlay[z] = glyph[dz]
grid.draw(overlay=path_overlay)
a = passwd(z, dz)

print("part a:", a)

w = 50

edges = {
    1: 10,
    2: 9,
    4: 5,
    6: 3,
    7: 8,
    11: 14,
    12: 13,
}
edges.update({v: k for k, v in edges.items()})

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
    1: (-1, 3),
    2: (-2, 3),
    4: (-1, 1),
    6: (1, -2),
    7: (-1, 1),
    11: (1, -2),
    12: (1, -1),
}


path_overlay = {z0: glyph[dz0]}
z = z0
dz = dz0
for step in steps:
    if step == "R":
        dz *= 1j
    elif step == "L":
        dz *= -1j
    else:
        for _ in range(step):
            next_z = z + dz
            next_dz = dz

            if grid.get(next_z, " ") == " ":
                if dz == 1:
                    y = z.imag
                    if 0 <= y < w:
                        edge = 3
                    elif w <= y < w * 2:
                        edge = 5
                    elif w * 2 <= y < w * 3:
                        edge = 6
                    else:
                        assert w * 3 <= y < w * 4
                        edge = 8
                elif dz == -1:
                    y = z.imag
                    if 0 <= y < w:
                        edge = 14
                    elif w <= y < w * 2:
                        edge = 13
                    elif w * 2 <= y < w * 3:
                        edge = 11
                    else:
                        assert w * 3 <= y < w * 4
                        edge = 10
                elif dz == 1j:
                    x = z.real
                    if 0 <= x < w:
                        edge = 9
                    elif w <= x < w * 2:
                        edge = 7
                    else:
                        assert w * 2 <= x < w * 3
                        edge = 4
                else:
                    assert dz == -1j
                    x = z.real
                    if 0 <= x < w:
                        edge = 12
                    elif w <= x < w * 2:
                        edge = 1
                    else:
                        assert w * 2 <= x < w * 3
                        edge = 2
                other_edge = edges[edge]
                if edge in rots:
                    next_dz = dz * rots[edge]
                else:
                    r = rots[other_edge]
                    if r == 1j:
                        r = -1j
                    next_dz = dz * r

                x = int(z.real)
                y = int(z.imag)
                x %= w
                y %= w
                if edge in offsets:
                    ox, oy = offsets[edge]
                else:
                    o1, o2 = offsets[other_edge]
                    ox, oy = -o1, -o2
                change_tile = ox*w + oy*1j*w
                if edge == 2 or edge == 9:
                    next_z = z + change_tile
                    if edge == 2:
                        next_z += (w - 1) * 1j
                    else:
                        assert edge == 9
                        next_z -= (w - 1) * 1j
                elif edge in (6, 11, 3, 14):
                    next_z = z + change_tile
                    # flip thing
                    next_z = next_z.real + (int(next_z.imag) // w ) * w * 1j + (w - 1 - y) * 1j
                else:
                    assert edge in (1, 4, 7, 12) or edge in (10, 5, 8, 13)
                    next_z = z + change_tile
                    next_z = (int(next_z.real) // w ) * w + (int(next_z.imag) // w) * w * 1j
                    next_z += y + x * 1j
            assert next_z in grid
            if grid[next_z] == "#":
                break
            path_overlay[next_z] = glyph[dz]

            z = next_z
            dz = next_dz
        path_overlay[z] = glyph[dz]

grid.draw(overlay=path_overlay)

print("part b:", passwd(z, dz))
