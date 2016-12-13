# coding: utf-8
from __future__ import unicode_literals
from aocd import data
from collections import deque
from itertools import cycle
import sys


def wall(x, y, n):
    w = x*x + 3*x + 2*x*y + y + y*y + n
    return '.#'[bin(w).count('1')%2]


def generate_office_space(h, w, fav_number=int(data)):
    office = [[0]*w for i in range(h)]
    for row in range(h):
        for col in range(w):
            office[row][col] = wall(x=col, y=row, n=fav_number)
    return office


def print_office(office):
    h = len(office)
    [w] = {len(row) for row in office}
    print('   ' + ' '.join([str(x)[-1] for x in range(w)]))
    for row in range(h):
        print(str(row).rjust(2).ljust(3) + ' '.join(office[row]))


def bfs(state0, target, office, verbose=True, max_depth=None):

    def progress_bar(msg, spinner=cycle(r'\|/-')):
        msg = ('\r{} '.format(next(spinner)) + msg).ljust(50)
        sys.stdout.write(msg)
        sys.stdout.flush()

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
                if verbose:
                    progress_bar(msg, spinner=iter('✖'))
                    sys.stdout.write('\n')
                err = Exception(msg)
                err.n_visited = len(seen) - 1
                raise err
        if new_depth > depth:
            depth = new_depth
        if state == target:
            if verbose:
                progress_bar('Target found at depth {}'.format(depth), spinner=iter('✔'))
                sys.stdout.write('\n')
            return depth
        else:
            if verbose and (i%2000 == 0):
                progress_bar('search depth {}, queue length {}'.format(new_depth, len(queue)))
        children = list(get_valid_next_states(state, office, seen=seen))
        seen.update(children)
        queue.extend((child, depth + 1) for child in children)


def get_valid_next_states(state, office, seen=()):
    directions = -1, 1, -1j, 1j  # left, right, up, down
    h = len(office)
    [w] = {len(row) for row in office}
    for direction in directions:
        new_state = state + direction
        row, col = int(new_state.imag), int(new_state.real)
        if 0 <= row < h and 0 <= col < w:  # we aren't stepping off the edge
            if office[row][col] != '#':  # we aren't walking into a wall
                if new_state not in seen:  # we haven't already been here
                    yield new_state



# state: complex number with (x, y) == (row, col) == (state.imag, state.real)
state0 = 1 + 1j
target = 7 + 4j
office = generate_office_space(h=7, w=10, fav_number=10)
assert bfs(state0, target, office, verbose=False) == 11

target = 31 + 39j
office = generate_office_space(h=50, w=50)
print(bfs(state0, target, office))  # part A: 92

try:
    bfs(state0, target, office, max_depth=50)
except Exception as err:
    n_locations = err.n_visited

print(n_locations)  # part B: 124
