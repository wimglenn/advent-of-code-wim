"""
--- Day 17: Pyroclastic Flow ---
https://adventofcode.com/2022/day/17
"""
from aocd import data
from aoc_wim.zgrid import ZGrid


sprites = """\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""


bricks = []
for sprite in sprites.split("\n\n"):
    g = ZGrid(sprite)
    zs = g.z("#", first=False)
    bricks.append((zs, g.width, g.height))


W = 7
Ta = 2022
Tb = 1000000000000
grid = ZGrid({x + 1j: "#" for x in range(W)})

seen = {}
a = i = top = i_push = 0
while i < Tb:
    i_brick = i % len(bricks)
    if i == Ta:
        a = top
    elif i > Ta:
        # index into bricks, index into moves, current "shape" of top row of grid
        shape = "".join([grid.get(x - top * 1j, ".") for x in range(W)])
        state = i_brick, i_push, shape
        if state in seen:
            i_prev, top_prev = seen[state]
            period = i - i_prev
            growth = top - top_prev
            n = (Tb - i) // period
            new_top = top + n * growth
            new_i = i + n * period
            # copy what the top of the grid looks like, and fast-forward time bigly
            for h in range(20):
                for x in range(W):
                    if x + (h - top) * 1j in grid:
                        grid[x + (h - new_top) * 1j] = "#"
            top = new_top
            i = new_i
            seen.clear()
        seen[state] = i, top

    brick, w, h = bricks[i_brick]
    p0 = 2 - (top + h + 2) * 1j
    g = ZGrid(dict.fromkeys(brick, "#"))
    g.offset(p0)
    x0 = p0.real
    while True:
        push = data[i_push]
        i_push = (i_push + 1) % len(data)
        if push == ">":
            if (x0 + w + 1).real <= W and not any(z + 1 in grid for z in g):
                g.offset(1)
                x0 += 1
        elif push == "<":
            if (x0 - 1).real >= 0 and not any(z - 1 in grid for z in g):
                g.offset(-1)
                x0 -= 1
        if any(z + 1j in grid for z in g):
            grid.update(g)
            top = max(top, int(1 - g.top_left.imag))
            break
        g.offset(1j)
    i += 1


print("part a:", a)
print("part b:", top)
