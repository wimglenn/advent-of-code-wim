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
    state0 = (1,)
    for k in chip_names:
        state0 += (chips[k],)
    for k in chip_names:
        state0 += (generators[k],)
    if not is_valid(state0):
        raise Exception("parsed state vector is invalid")
    return state0


def is_valid(state):
    n = len(state) // 2
    elevator = state[0]
    chips = state[1:1+n]
    generators = state[1+n:]
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


class Q11AStar(AStar):

    def __init__(self, data, part="a"):
        state0 = parsed(data)
        self.n = n = len(state0) // 2
        target = (4,) * (2 * n + 1)
        if part == "b":
            state0 = state0[:1 + n] + (1, 1) + state0[1 + n:] + (1, 1)
            target += (4,) * 4
            self.n += 2
        AStar.__init__(self, state0, target)

    def heuristic(self, state0, state1):
        return sum(abs(a - b) for (a, b) in zip(state0, state1))

    def adjacent(self, state):
        n = self.n
        elevator = state[0]
        chips = state[1:n]
        generators = state[n:]
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
            new_state = (new_elevator,) + tuple(new_chips) + tuple(new_generators)
            if is_valid(new_state):
                yield new_state

    cost = heuristic


a = Q11AStar(data, part="a")
a.run()
print("part a:", a.path_length)

b = Q11AStar(data, part="b")
b.run()
print("part b:", b.path_length)
