from collections import deque
from itertools import product, combinations


data = 'test'
data = 'part1'
data = 'part2'

# state vector structure: 3-tuple of (int, tuple, tuple) 
# (elevator_floor, (chip1_floor, chip2_floor, ..., chipN_floor), (generator1_floor, generator2_floor, ..., generatorN_floor))

if data == 'test':
    state0 = (1, (1,1), (2,3))
    target = (4, (4,4), (4,4))

if data == 'part1':
    state0 = (1, (1,2,2,3,3), (1,1,1,3,3))
    target = (4, (4,4,4,4,4), (4,4,4,4,4))

if data == 'part2':
    state0 = (1, (1,2,2,3,3,1,1), (1,1,1,3,3,1,1))
    target = (4, (4,4,4,4,4,4,4), (4,4,4,4,4,4,4))


def is_valid(state):
    elevator, chips, generators = state
    for chip, generator in zip(chips, generators):
        if chip != generator:  # if the chip and the matching generator are on different floors
            if chip in generators:  # and there is some other generator on the same floor as the chip
                return False  # then this chip gets fried
    if not {elevator}.union(chips, generators) < {1, 2, 3, 4}:
        return False  # everything must be on a floor 1-4
    if elevator not in set().union(chips, generators):
        return False  # it's impossible for the elevator to be on an empty floor
    return True


def get_valid_next_states(state, seen=()):
    elevator, chips, generators = state
    items = list(chips + generators)
    # indices of stuff on the same floor as the elevator:
    indices = [i for i, item_pos in enumerate(items) if elevator == item_pos]
    # we can take 1 or 2 things with us when changing floors
    indices_choices = list(combinations(indices, 1)) + list(combinations(indices, 2))
    # we can go up or down a floor
    directions = -1, +1
    for direction, indices in product(directions, indices_choices):
        new_elevator = elevator + direction
        new_items = items[:]
        for index in indices:
            new_items[index] += direction
        new_chips = new_items[:len(chips)]
        new_generators = new_items[len(chips):]
        assert len(new_chips) == len(chips)
        assert len(new_generators) == len(generators)
        new_state = new_elevator, tuple(new_chips), tuple(new_generators)
        if is_valid(new_state) and new_state not in seen:
            yield new_state


def bfs(state0, target):
    depth = 0
    queue = deque([(state0, depth)])
    seen = {state0}
    while queue:
        state, new_depth = queue.popleft()
        if new_depth > depth:
            print('search depth {}, queue length {}'.format(new_depth, len(queue)))
            depth = new_depth
        if state == target:
            return depth
        children = list(get_valid_next_states(state, seen))
        seen.update(children)
        queue.extend((child, depth + 1) for child in children)


assert(is_valid(state0) and is_valid(target))
print(bfs(state0, target))

# part1: 31
# part2: 55
