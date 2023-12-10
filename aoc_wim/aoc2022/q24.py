"""
--- Day 24: Blizzard Basin ---
https://adventofcode.com/2022/day/24
"""
from aocd import data

from aoc_wim.zgrid import ZGrid


grid = ZGrid(data)
grid.offset(-1-1j)
h = grid.height - 2
w = grid.width - 2
min_depth = h + w

bu = grid.z("^", first=False)
br = grid.z(">", first=False)
bd = grid.z("v", first=False)
bl = grid.z("<", first=False)


empty = ZGrid({z: ".#"[g == "#"] for z, g in grid.items()})
z_start = -1j
z_end = w - 1 + h * 1j


rep = dict.fromkeys("^>v<", "2")
rep["2"] = "3"
rep["3"] = "4"


def bliz(t):
    g = ZGrid(empty)
    u_y = [(int(z.imag) - t) % h for z in bu]
    r_x = [(int(z.real) + t) % w for z in br]
    d_y = [(int(z.imag) + t) % h for z in bd]
    l_x = [(int(z.real) - t) % w for z in bl]
    u = [z.real + 1j * y for z, y in zip(bu, u_y)]
    r = [x + 1j * z.imag for z, x in zip(br, r_x)]
    d = [z.real + 1j * y for z, y in zip(bd, d_y)]
    l = [x + 1j * z.imag for z, x in zip(bl, l_x)]
    g.update(dict.fromkeys(u, "^"))
    g.update({z: rep.get(g[z], ">") for z in r})
    g.update({z: rep.get(g[z], "v") for z in d})
    g.update({z: rep.get(g[z], "<") for z in l})
    return g


def fill(z, targets):
    zs = {z}
    m = -1
    while targets:
        target = targets.pop()
        while target not in zs:
            m += 1
            g = bliz(m)
            zs = {z for z0 in zs for z in g.near(z0, n=5) if g.get(z) == "."}
        zs = {target}
    return m


print("answer_a:", fill(z=z_start, targets=[z_end]))
print("answer_b:", fill(z=z_start, targets=[z_end, z_start, z_end]))
