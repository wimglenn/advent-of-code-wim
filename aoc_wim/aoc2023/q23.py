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
for z, g in grid.items():
    if g == "." and sum(grid.get(z + dz) in dzs for dz in dzs.values()) >= 2:
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


def longest_path(part="a"):
    grid[start + 1j] = "v"
    paths = []
    stack = [(start, 0)]
    while stack:
        path = stack.pop()
        z0, d0 = path[-2:]
        if z0 == end:
            paths.append(path)
        branches = nodes[z0]
        for g, dz in dzs.items():
            if dz in branches and grid[z0 + dz] in ([g] if part == "a" else dzs):
                z1, dist = branches[dz]
                if z1 not in path:
                    stack.append(path + (z1, d0 + dist))
    return max(p[-1] for p in paths)


print("answer_a:", longest_path(part="a"))
print("answer_b:", longest_path(part="b"))
