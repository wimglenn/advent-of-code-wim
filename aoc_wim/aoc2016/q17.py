"""
--- Day 17: Two Steps Forward ---
https://adventofcode.com/2016/day/17
"""
from collections import deque
from _md5 import md5
from aocd import data


def bfs(part="a"):
    z0 = 0
    target = 3 + 3j
    depth = 0
    path = ""
    longest_path_length = None
    queue = deque([(z0, path, depth)])
    while queue:
        z, path, depth = queue.popleft()
        if z == target:
            if part == "a":
                return path
            longest_path_length = depth
        else:
            queue.extend((x + (depth + 1,)) for x in adjacent(z, path))
    return longest_path_length


def adjacent(z0, path):
    dzs = {"U": -1j, "D": 1j, "L": -1, "R": 1}
    directions = zip(dzs.items(), md5((data + path).encode()).hexdigest())
    for (dpath, dz), s in directions:
        if s in "bcdef":
            z = z0 + dz
            if 0 <= z.real <= 3 and 0 <= z.imag <= 3:
                yield z, path + dpath


print("part a:", bfs(part="a"))
print("part b:", bfs(part="b"))
