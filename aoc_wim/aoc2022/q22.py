"""
--- Day 22: Monkey Map ---
https://adventofcode.com/2022/day/22
"""
from aocd import data

g, code = data.split("\n\n")

steps = []
while "L" in code or "R" in code:
    if code[:1] in "LR":
        steps.append(code[0])
        code = code[1:]
    else:
        iL = None
        if "L" in code:
            iL = code.index("L")
        iR = None
        if "R" in code:
            iR = code.index("R")
        if iL is None:
            iL = iR
        if iR is None:
            iR = iL
        n = code[:min(iL, iR)]
        steps.append(int(n))
        code = code[len(n):]
steps.append(int(code))

grid = ZGrid(g)

# grid.draw()
z0 = grid.z(".")
z_blank = grid.z(" ", first=False)
for z in z_blank:
    del grid.d[z]
dz0 = 1


facing = {
    1: 0,
    1j: 1,
    -1: 2,
    -1j: 3,
}

def passwd(z, dz):
    return int(1000*(z.imag+1) + 4*(z.real+1) + facing[dz])


next_zs = {}
z = z0
dz = dz0
for step in steps:
    if step == "R":
        dz *= 1j
    elif step == "L":
        dz *= -1j
    else:
        assert isinstance(step, int)
        for _ in range(step):
            next_z = z + dz
            if next_z not in grid:
                next_z = z
                while next_z in grid:
                    next_z -= dz
                next_z += dz
            assert next_z in grid
            if grid[next_z] == "#":
                break
            next_zs[next_z] = "^" if dz == -1j else ">" if dz == 1 else "v" if dz == 1j else "<"
            z = next_z

overlay = next_zs | {b: " " for b in z_blank}
# grid.draw(overlay=next_zs)

a = passwd(z, dz)

print("part a:", a)
import sys

H = grid.height
W = grid.width
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
edgesi = {v: k for k, v in edges.items()}
edges.update(edgesi)

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


d = dict(zip(range(w), reversed(range(w))))

next_zs = {}
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

            if next_z not in grid:
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
                    next_z = next_z.real + (int(next_z.imag) // w ) * w * 1j + d[y] * 1j
                else:
                    assert edge in (1, 4, 7, 12) or edge in (10, 5, 8, 13)
                    next_z = z + change_tile
                    next_z = (int(next_z.real) // w ) * w +  (int(next_z.imag) // w ) * w * 1j
                    next_z += y + x * 1j
            assert next_z in grid
            if grid[next_z] == "#":
                break
            next_zs[next_z] = "^" if dz == -1j else ">" if dz == 1 else "v" if dz == 1j else "<"

            z = next_z
            dz = next_dz

overlay = next_zs | {b: " " for b in z_blank}
grid.draw(overlay=next_zs)

print("part b:", passwd(z, dz))
