"""
--- Day 23: A Long Walk ---
https://adventofcode.com/2023/day/23
"""
from aocd import data

from aoc_wim.zgrid import ZGrid


grid = ZGrid(data)
start = 1
end = grid.bottom_right - 1

nodes = {}
dzs = dict(zip("^>v<", [-1j, 1, 1j, -1]))
for z in grid.z(".", first=False):
    if sum(grid.get(z + dz) in dzs for dz in dzs.values()) >= 2:
        nodes[z] = {}


def find_next_node(z0, dz0):
    path = [z0, z0 + dz0]
    while path[-1] not in nodes:
        [z1] = [z for z in grid.near(path[-1]) if z != path[-2] and grid.get(z, "#") != "#"]
        path.append(z1)
    return path[-1], path[-2] - path[-1], len(path) - 1


nodes[start] = {1j: find_next_node(start, 1j)}
nodes[end] = {-1j: find_next_node(end, -1j)}
for z0, branches in nodes.items():
    for dz0 in dzs.values():
        g = grid.get(z0 + dz0)
        if g in dzs and dz0 not in branches:
            z1, dz1, dist = find_next_node(z0, dz0)
            branches[dz0] = z1, dist
            nodes[z1][dz1] = z0, dist
perimeter = {z for z, branches in nodes.items() if len(branches) < 4}



def longest_path(part="a"):
    grid[start + 1j] = "v"
    dists = []
    stack = [(start, {start}, 0)]
    while stack:
        z0, visited, d0 = stack.pop()
        if z0 == end:
            dists.append(d0)
        branches = nodes[z0]
        for g, dz in dzs.items():
            if dz in branches:
                z1, dist = branches[dz]
                if z1 in visited:
                    continue
                if grid[z0 + dz] != g:
                    if part == "a" or {z0, z1} <= perimeter:
                        continue
                stack.append((z1, visited.union([z1]), d0 + dist))
    return max(dists)


print("answer_a:", longest_path(part="a"))
print("answer_b:", longest_path(part="b"))
