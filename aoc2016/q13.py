# coding: utf-8
from __future__ import unicode_literals
from aocd import data
from collections import deque, defaultdict
from itertools import cycle
from operator import attrgetter
import sys


class Maze(object):

    # up, down, left, right
    wallmap = {
        (0, 0, 0, 0): '■',
        (0, 0, 0, 1): '╺',
        (0, 0, 1, 0): '╸',
        (0, 0, 1, 1): '━',
        (0, 1, 0, 0): '╻',
        (0, 1, 0, 1): '┏',
        (0, 1, 1, 0): '┓',
        (0, 1, 1, 1): '┳',
        (1, 0, 0, 0): '╹',
        (1, 0, 0, 1): '┗',
        (1, 0, 1, 0): '┛',
        (1, 0, 1, 1): '┻',
        (1, 1, 0, 0): '┃',
        (1, 1, 0, 1): '┣',
        (1, 1, 1, 0): '┫',
        (1, 1, 1, 1): '╋',
    }
    # wallmap = defaultdict(lambda: '#')
    wallmap.update({
        'open space': ' ',
        'place seen': '.',
        'start spot': 'o',
        'the target': 'X',
    })

    def __init__(self, fav_number=int(data)):
        self.fav_number = fav_number
        self.memo = {}

    def is_wall(self, state):
        if state not in self.memo:
            y, x = int(state.imag), int(state.real)
            if x < 0 or y < 0:
                self.memo[state] = 1
            else:
                z = (x+y)**2 + 3*x + y
                self.memo[state] = bin(z + self.fav_number).count('1') % 2
        return self.memo[state]

    def valid_next_states(self, state, seen=()):
        deltas = -1j, +1j, -1, +1
        neighbours = [state + delta for delta in deltas]
        for z in neighbours:
            if not self.is_wall(z) and z not in seen:
                yield z

    def get_char(self, x, y, visited=(), start=None, end=None):
        state = complex(x, y)
        if state == start:
            # assert 0
            return self.wallmap['start spot']
        elif state == end:
            return self.wallmap['the target']
        elif state in visited:
            return self.wallmap['place seen']
        elif not self.is_wall(state):
            return self.wallmap['open space']
        # up, down, left, right
        deltas = -1j, +1j, -1, +1
        walls = [self.is_wall(state+d) for d in deltas]
        return self.wallmap[tuple(walls)]

    def display(self, w=None, h=None, visited=(), start=None, end=None):
        if not self.memo:
            # prevents max on an empty sequence
            self.is_wall(complex(50, 50))
        if w is None:
            w = max([int(x.real) for x in self.memo]) + 1
        if h is None:
            h = max([int(x.imag) for x in self.memo]) + 1
        for y in range(h):
            row = [self.get_char(x, y, visited=visited, start=start, end=end) for x in range(w)]
            line = ''.join(row)
            print(line)


class MaxDepth(Exception):
    pass


def bfs(state0, target, maze, max_depth=None):
    depth = 0
    queue = deque([(state0, depth)])
    seen = {state0}
    i = 0
    while queue:
        state, new_depth = queue.popleft()
        i += 1
        if max_depth is not None:
            if new_depth > max_depth:
                msg = 'Aborting at depth {}'.format(max_depth)
                err = MaxDepth(msg)
                err.n_visited = len(seen) - len(queue) - 1
                err.seen = seen
                raise err
        if new_depth > depth:
            depth = new_depth
        if state == target:
            return depth
        children = list(maze.valid_next_states(state, seen=seen))
        seen.update(children)
        queue.extend((child, depth + 1) for child in children)


def n_points_within_distance(state0, maze, d=50):
    target = -1  # just any impossible-to-find state
    try:
        bfs(state0, target, maze, max_depth=d)
    except MaxDepth as err:
        return err.n_visited


# state: complex number with (x, y) == (row, col) == (state.imag, state.real)
state0 = 1+1j
test_maze = Maze(fav_number=10)
# test_maze.display(h=7, w=10)
assert bfs(state0, target=7+4j, maze=test_maze) == 11

target = 31 + 39j
maze = Maze()
print(bfs(state0, target, maze))  # part A: 92
print(n_points_within_distance(state0, maze))  # part B: 124


others_data = {
    'kevin': (1362, 82, 138),
    'davidism': (1350, 92, 124),
    'dsm': (1358, 96, 141),
    'andras': (1364, 86, 127),
}
for name, (fav_number, partA, partB) in others_data.items():
    other_maze = Maze(fav_number=fav_number)
    assert bfs(state0, target, other_maze) == partA
    assert n_points_within_distance(state0, other_maze) == partB
