from itertools import combinations
from itertools import product

from aocd import data
from aoc_wim.search import AStar


def parsed(data):
    """
    state vector structure: 3-tuple of (int, tuple, tuple) 
    (
        elevator_floor, 
        (chip1_floor, chip2_floor, ... chipN_floor), 
        (genr1_floor, genr2_floor, ... genrN_floor),
    )
    """
    chips = {}
    generators = {}
    for line_no, line in enumerate(data.splitlines(), 1):
        words = line.split()
        for i, word in enumerate(words, -1):
            if word.startswith("generator"):
                generator = words[i]
                generators[generator] = line_no
            elif word.startswith("microchip"):
                chip, compatible = words[i].split("-")
                chips[chip] = line_no
    chip_names = sorted(chips)
    if chip_names != sorted(generators):
        raise Exception("chip and generators mismatched")
    state0 = (
        1,
        tuple(chips[k] for k in chip_names),
        tuple(generators[k] for k in chip_names),
    )
    target = 4, tuple(4 for c in chip_names), tuple(4 for g in generators)
    if not is_valid(state0) or not is_valid(target):
        raise Exception("parsed state vector is invalid")
    return state0, target


def is_valid(state):
    elevator, chips, generators = state
    for chip, generator in zip(chips, generators):
        if chip != generator:
            # if the chip and the matching generator are on different floors
            if chip in generators:
                # and there is some other generator on the same floor as the chip
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
        new_chips = new_items[: len(chips)]
        new_generators = new_items[len(chips) :]
        assert len(new_chips) == len(chips)
        assert len(new_generators) == len(generators)
        new_state = new_elevator, tuple(new_chips), tuple(new_generators)
        if is_valid(new_state) and new_state not in seen:
            yield new_state


class Q11AStar(AStar):

    def __init__(self, data, part="a"):
        state0, target = parsed(data)
        if part == "b":
            state0 = state0[0], state0[1] + (1, 1), state0[2] + (1, 1)
            target = target[0], target[1] + (4, 4), target[2] + (4, 4)
        AStar.__init__(self, state0, target)

    def heuristic(self, state0, state1):
        elevator0, chips0, generators0 = state0
        elevator1, chips1, generators1 = state0
        result = abs(elevator0 - elevator1)
        for c0, c1 in zip(chips0, chips1):
            result += abs(c0 - c1)
        for g0, g1 in zip(generators0, generators1):
            result += abs(g0 - g1)
        return result

    def adjacent(self, state):
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
            new_chips = new_items[: len(chips)]
            new_generators = new_items[len(chips):]
            assert len(new_chips) == len(chips)
            assert len(new_generators) == len(generators)
            new_state = new_elevator, tuple(new_chips), tuple(new_generators)
            if is_valid(new_state):
                yield new_state

    cost = heuristic


a = Q11AStar(data, part="a")
a.run()
print("part a:", a.path_length)

b = Q11AStar(data, part="b")
b.run()
print("part b:", b.path_length)
