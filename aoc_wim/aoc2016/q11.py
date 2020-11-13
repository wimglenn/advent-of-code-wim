"""
--- Day 11: Radioisotope Thermoelectric Generators ---
https://adventofcode.com/2016/day/11
"""
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
    pairs = [(chips[k], generators[k]) for k in chips]
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

    cost = heuristic

    def adjacent(self, state):
        # indices of stuff on the same floor as the elevator
        idx = [i for i in range(1, len(state)) if state[0] == state[i]]
        # we can take 1 or 2 things with us when changing floors
        idx_choices = [*combinations(idx, 1), *combinations(idx, 2)]
        # we can go up or down a floor, unless on ground (1) or top (4)
        s0s = {1: (2,), 4: (3,)}.get(state[0], (state[0] - 1, state[0] + 1))
        for s0, idx in product(s0s, idx_choices):
            next_state = [s0] + list(state[1:])
            for i in idx:
                next_state[i] = s0
            pairs = zip(next_state[1::2], next_state[2::2])
            next_state = sum(sorted(pairs), (s0,))
            if is_valid(next_state):
                yield next_state


a = Q11AStar(data, part="a")
a.run()
print("part a:", a.path_length)

b = Q11AStar(data, part="b")
b.run()
print("part b:", b.path_length)
