"""
--- Day 23: Unstable Diffusion ---
https://adventofcode.com/2022/day/23
"""
from collections import defaultdict
from collections import deque

from aocd import data

from aoc_wim.zgrid import ZGrid


grid = ZGrid(data, transform={".": None})
edges = deque([
    (-1j - 1, -1j, -1j + 1),
    (+1j - 1, +1j, +1j + 1),
    (-1j - 1,  -1, +1j - 1),
    (-1j + 1,  +1, +1j + 1),
])


def movers():
    d = defaultdict(list)  # dest: sources
    for z0 in grid:
        elves_nearby = {e[1]: sum(z0 + dz in grid for dz in e) for e in edges}
        if sum(elves_nearby.values()):
            for dz, n_nearby in elves_nearby.items():
                if not n_nearby:
                    d[z0 + dz].append(z0)
                    break
    return {z: zs[0] for z, zs in d.items() if len(zs) == 1}  # dest: source


# grid.draw(title="== Initial State == ")
i = 0
a = b = None
while a is None or b is None:
    i += 1
    z1_z0 = movers()
    grid.d = dict.fromkeys(grid.keys() - z1_z0.values() | z1_z0.keys(), "#")
    # grid.draw(title=f"== End of round {i} ==")
    edges.rotate(-1)
    if b is None and not z1_z0:  # nobody moved
        b = i
    if a is None and i == 10:
        a = grid.area - len(grid)

print("answer_a:", a)
print("answer_b:", b)
