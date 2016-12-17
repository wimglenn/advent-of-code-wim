from __future__ import unicode_literals
from aocd import data
from collections import deque
from hashlib import md5


def bfs(state0, target, next_states, max_depth=None, mode='shortest'):
    z0, key = state0
    depth = 0
    queue = deque([(state0, depth)])
    best_depth = None
    i = 0
    while queue:
        (z, path), new_depth = queue.popleft()
        i += 1
        if new_depth > depth:
            depth = new_depth
        if z == target:
            if mode == 'shortest':
                return path[len(key):]
            else:
                assert mode == 'longest'
                best_depth = new_depth if best_depth is None else max(best_depth, new_depth)
        children = list(next_states((z, path)))
        if max_depth is None or depth < max_depth:
            queue.extend((child, depth + 1) for child in children)
    return best_depth


def next_states(state):
    offsets = {'U': 1j, 'D': -1j, 'L': -1, 'R': 1}
    z0, path = state
    if z0 == 3 - 3j:
        return
    directions = zip('UDLR', md5(path.encode()).hexdigest())
    for dir_, s in directions:
        if s in 'bcdef':
            z1 = z0 + offsets[dir_]
            if -3 <= z1.imag <= 0 <= z1.real <= 3:
                yield z1, path + dir_


# state vector: tuple of (z, str_)
#   z: a complex number representing position
#   str_: a string representing the passcode + the path so far
z0 = 0
target = 3 - 3j
state0 = z0, data


assert bfs((z0, 'hijkl'),    target, next_states, mode='shortest') is None
assert bfs((z0, 'ihgpwlah'), target, next_states, mode='shortest') == 'DDRRRD'
assert bfs((z0, 'kglvqrro'), target, next_states, mode='shortest') == 'DDUDRLRRUDRD'
assert bfs((z0, 'ulqzkmiv'), target, next_states, mode='shortest') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'
print(bfs(state0, target, next_states, mode='shortest'))  # part a: RDURRDDLRD

assert bfs((z0, 'hijkl'),    target, next_states, mode='longest') is None
assert bfs((z0, 'ihgpwlah'), target, next_states, mode='longest') == 370
assert bfs((z0, 'kglvqrro'), target, next_states, mode='longest') == 492
assert bfs((z0, 'ulqzkmiv'), target, next_states, mode='longest') == 830
print(bfs(state0, target, next_states, mode='longest'))  # part b: 526
