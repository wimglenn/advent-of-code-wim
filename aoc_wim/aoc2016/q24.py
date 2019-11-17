from collections import deque
from itertools import combinations
from itertools import permutations

import numpy as np
from aocd import data


test_data = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""


def valid_next_states(state, maze, seen=()):
    deltas = -1j, +1j, -1, +1
    neighbours = [state + dz for dz in deltas]
    for z in neighbours:
        row, col = int(-z.imag), int(z.real)
        if maze[row, col] != "#" and z not in seen:
            yield z


def bfs(state0, target, maze):
    depth = 0
    queue = deque([(state0, depth)])
    seen = {state0}
    while queue:
        state, this_depth = queue.popleft()
        depth = max(depth, this_depth)
        if state == target:
            return depth
        children = list(valid_next_states(state, maze, seen=seen))
        queue.extend((child, depth + 1) for child in children)
        seen.update(children)


def get_distance_matrix(data):
    maze = np.array([list(line) for line in data.splitlines()], dtype="<U1")
    targets = sorted([x for x in data if x.isdigit()])
    n = len(targets)

    states = []
    for target in targets:
        [row], [col] = np.where(maze == target)
        states.append(complex(col, -row))

    d = np.zeros((n, n), dtype=int)
    for a, b in combinations(range(n), 2):
        d[a, b] = d[b, a] = bfs(states[a], states[b], maze)

    return d


def solve(d, return_home=False):
    distance = {}
    for path in permutations(range(1, len(d))):
        path = (0,) + path + ((0,) if return_home else ())
        distance[path] = sum(d[a, b] for a, b in zip(path, path[1:]))
    return min(distance.values())


test_d = get_distance_matrix(test_data)
assert solve(test_d, return_home=0) == 14
assert solve(test_d, return_home=1) == 20

d = get_distance_matrix(data)
print(solve(d, return_home=0))
print(solve(d, return_home=1))
