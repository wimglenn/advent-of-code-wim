from collections import deque
from hashlib import md5

from aocd import data


def bfs(state0, target, next_states, max_depth=None, mode="shortest"):
    z0, key = state0
    depth, best_depth = 0, None
    queue = deque([(state0, depth)])
    i = 0
    while queue:
        (z, path), depth = queue.popleft()
        i += 1
        if z == target:
            if mode == "shortest":
                return path[len(key) :]
            else:
                assert mode == "longest"
                best_depth = depth
        children = list(next_states((z, path)))
        if max_depth is None or depth < max_depth:
            queue.extend((child, depth + 1) for child in children)
    return best_depth


def next_states(state):
    offsets = {"U": 1j, "D": -1j, "L": -1, "R": 1}
    z0, path = state
    if z0 == 3 - 3j:
        return
    directions = zip("UDLR", md5(path.encode()).hexdigest())
    for dir_, s in directions:
        if s in "bcdef":
            z1 = z0 + offsets[dir_]
            if -3 <= z1.imag <= 0 <= z1.real <= 3:
                yield z1, path + dir_


# state vector: tuple of (z, str_)
#   z: a complex number representing position
#   str_: a string representing the passcode + the path so far
z0 = 0
target = 3 - 3j
state0 = z0, data


tests_a = {
    # code: shortest path
    "hijkl": None,
    "ihgpwlah": "DDRRRD",
    "kglvqrro": "DDUDRLRRUDRD",
    "ulqzkmiv": "DRURDRUDDLLDLUURRDULRLDUUDDDRR",
}
for code, path in tests_a.items():
    assert bfs((z0, code), target, next_states, mode="shortest") == path


tests_b = {"hijkl": None, "ihgpwlah": 370, "kglvqrro": 492, "ulqzkmiv": 830}

for code, path in tests_b.items():
    assert bfs((z0, code), target, next_states, mode="longest") == path


print(bfs(state0, target, next_states, mode="shortest"))
print(bfs(state0, target, next_states, mode="longest"))
