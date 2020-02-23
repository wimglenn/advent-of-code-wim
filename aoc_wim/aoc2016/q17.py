from collections import deque
from _md5 import md5
from aocd import data


def bfs(state0=(0, data), target=3 + 3j, part="a"):
    z0, key = state0
    depth, longest_path_length = 0, None
    queue = deque([(state0, depth)])
    while queue:
        (z, path), depth = queue.popleft()
        if z == target:
            if part == "a":
                return path[len(key) :]
            else:
                longest_path_length = depth
        queue.extend((child, depth + 1) for child in next_states((z, path)))
    return longest_path_length


def next_states(state):
    offsets = {"U": -1j, "D": 1j, "L": -1, "R": 1}
    z0, path = state
    if z0 == 3 + 3j:
        return
    directions = zip(offsets, md5(path.encode()).hexdigest())
    for dir_, s in directions:
        if s in "bcdef":
            z1 = z0 + offsets[dir_]
            if 0 <= z1.real <= 3 and 0 <= z1.imag <= 3:
                yield z1, path + dir_


print("part a:", bfs(part="a"))
print("part b:", bfs(part="b"))
