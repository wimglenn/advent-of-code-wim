"""
--- Day 10: Knot Hash ---
https://adventofcode.com/2017/day/10
"""
from functools import reduce
from operator import xor

from aocd import data


def munge(state, lengths, iterations=64):
    n = len(state)
    skip_size = 0
    current_position = 0
    for i in range(iterations):
        for length in lengths:
            for i in range(length // 2):
                i1 = (current_position + i) % n
                i2 = (current_position + length - i - 1) % n
                state[i1], state[i2] = state[i2], state[i1]
            current_position += length + skip_size
            skip_size += 1


try:
    lengths = [int(x) for x in data.split(",")]
except ValueError:
    pass
else:
    state = list(range(5 if data == "3, 4, 1, 5" else 256))
    munge(state, lengths, 1)
    print("part a:", state[0] * state[1])

state = list(range(256))
lengths = [ord(x) for x in data] + [17, 31, 73, 47, 23]
munge(state, lengths)
reduced = [reduce(xor, state[16 * i : 16 * (i + 1)], 0) for i in range(16)]
print("part b:", bytes(reduced).hex())
