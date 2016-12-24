from aocd import data
import numpy as np
from collections import deque
from itertools import permutations, combinations


test_data = '''
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
'''.strip()


def valid_next_states(state, maze, seen=()):
    deltas = -1j, +1j, -1, +1
    neighbours = [state + dz for dz in deltas]
    for z in neighbours:
        row, col = int(-z.imag), int(z.real)
        if maze[row,col] != '#' and z not in seen:
            yield z


def bfs(state0, target, maze):
    depth = 0
    queue = deque([(state0, depth)])
    seen = {state0}
    while queue:
        state, new_depth = queue.popleft()
        if new_depth > depth:
            depth = new_depth
        if state == target:
            return depth
        children = list(valid_next_states(state, maze, seen=seen))
        queue.extend((child, depth + 1) for child in children)
        seen.update(children)
    bfs.n_visited = len(seen)


def get_distance_matrix(data):
    n_rows = 1 + data.count('\n')
    maze = np.fromstring(data.replace('\n',''), dtype='S1').reshape(n_rows, -1).astype('U1')
    targets = sorted([x for x in data if x.isdigit()])
    n = len(targets)

    states = []
    for target in targets:
        [row], [col] = np.where(maze==target)
        states.append(complex(col, -row))

    d = np.zeros((n,n), dtype=int)
    for a,b in combinations(range(n), 2):
        d[a,b] = d[b,a] = bfs(states[a], states[b], maze)

    return d


def solve(d, return_home=False):
    d_min = float('inf')
    n = len(d)
    for order in permutations(range(1, n)):
        order = (0,) + order
        if return_home:
            order += (0,)
        d_total = sum(d[a,b] for a,b in zip(order, order[1:]))
        d_min = min(d_total, d_min)
    return d_min


test_d = get_distance_matrix(test_data)
assert solve(test_d, return_home=0) == 14
assert solve(test_d, return_home=1) == 20

d = get_distance_matrix(data)
print(solve(d, return_home=0))  # part a: 518
print(solve(d, return_home=1))  # part b: 716
