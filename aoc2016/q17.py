from aocd import data
from collections import deque
from hashlib import md5


def bfs(state0, target, next_states, max_depth=None, mode='shortest'):
    key = state0[1]
    depth = 0
    queue = deque([(state0, depth)])
    best_depth = None
    i = 0
    while queue:
        state, new_depth = queue.popleft()
        i += 1
        if new_depth > depth:
            depth = new_depth
        if state[0] == target:
            if mode == 'shortest':
                path = state[1][len(key):]
                return path
            else:
                assert mode == 'longest'
                best_depth = new_depth if best_depth is None else max(best_depth, new_depth)
        children = list(next_states(state))
        if max_depth is None or depth < max_depth:
            queue.extend((child, depth + 1) for child in children)
    return best_depth

'''
 0  1  2  3
 4  5  6  7
 8  9 10 11
12 13 14 15
'''

candidates = {
    0: 'RD',
    1: 'RDL',
    2: 'RDL',
    3: 'DL',
    4: 'URD',
    5: 'URDL',
    6: 'URDL',
    7: 'UDL',
    8: 'URD',
    9: 'URDL',
    10: 'URDL',
    11: 'UDL',
    12: 'UR',
    13: 'URL',
    14: 'URL',
    15: '',
}

offsets = {
    'U': -4,
    'D': +4,
    'L': -1,
    'R': +1,
}


def next_states(state):
    pos, path = state
    choices = candidates[pos]
    directions = zip('UDLR', md5(path).hexdigest()[:4])
    for dir_, s in directions:
        if s in 'bcdef' and dir_ in choices:
            yield pos + offsets[dir_], path + dir_


pos = 0
target = 15


assert bfs((pos, 'hijkl'), target, next_states, mode='shortest') is None
assert bfs((pos, 'ihgpwlah'), target, next_states, mode='shortest') == 'DDRRRD'
assert bfs((pos, 'kglvqrro'), target, next_states, mode='shortest') == 'DDUDRLRRUDRD'
assert bfs((pos, 'ulqzkmiv'), target, next_states, mode='shortest') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'
print(bfs((0, data), target, next_states, mode='shortest'))  # part a: RDURRDDLRD

assert bfs((pos, 'hijkl'), target, next_states, mode='longest') is None
assert bfs((pos, 'ihgpwlah'), target, next_states, mode='longest') == 370
assert bfs((pos, 'kglvqrro'), target, next_states, mode='longest') == 492
assert bfs((pos, 'ulqzkmiv'), target, next_states, mode='longest') == 830
print(bfs((0, data), target, next_states, mode='longest'))  # part b: 526
