from itertools import combinations
from itertools import product

from aocd import data
from aoc_wim.search import AStar


def parsed(data):
    """
    state vector structure:
    (elevator, chip1, gen1, chip2, gen2 ... chipN, genN)
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
    assert sorted(chips) == sorted(generators), "chip and generators mismatched"
    pairs = sorted([(chips[k], generators[k]) for k in chips])
    state0 = sum(pairs, (1,))
    assert is_valid(state0), "initial state vector is invalid"
    return state0


def is_valid(state):
    chips = state[1::2]
    generators = state[2::2]
    for chip, generator in zip(chips, generators):
        if chip != generator:
            # if the chip and the matching generator are on different floors
            if chip in generators:
                # and there is some other generator on the same floor as the chip
                return False  # then this chip gets fried
    return True


class Q11AStar(AStar):

    def __init__(self, data, part="a"):
        state0 = parsed(data)
        if part == "b":
            state0 += (1,) * 4
        target = (4,) * len(state0)
        AStar.__init__(self, state0, target)

    def heuristic(self, state0, state1):
        return sum([abs(a - b) for (a, b) in zip(state0, state1)])

    def adjacent(self, state):
        elevator = state[0]
        chips = state[1::2]
        generators = state[2::2]
        items = list(chips + generators)
        # indices of stuff on the same floor as the elevator:
        indices = [i for i, item_pos in enumerate(items) if elevator == item_pos]
        # we can take 1 or 2 things with us when changing floors
        indices_choices = list(combinations(indices, 1)) + list(combinations(indices, 2))
        # we can go up or down a floor
        directions = {1: (+1,), 2: (-1, +1), 3: (-1, +1), 4: (-1,)}[elevator]
        for direction, indices in product(directions, indices_choices):
            new_elevator = elevator + direction
            new_items = items[:]
            for index in indices:
                new_items[index] += direction
            new_chips = new_items[: len(chips)]
            new_generators = new_items[len(chips):]
            new_pairs = sorted([p for p in zip(new_chips, new_generators)])
            new_state = sum(new_pairs, (new_elevator,))
            if is_valid(new_state):
                yield new_state

    cost = heuristic


a = Q11AStar(data, part="a")
a.run()
print("part a:", a.path_length)

b = Q11AStar(data, part="b")
b.run()
print("part b:", b.path_length)
