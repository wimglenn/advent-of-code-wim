"""
--- Day 5: A Maze of Twisty Trampolines, All Alike ---
https://adventofcode.com/2017/day/5
"""
from aocd import data


def part_a(data, b_offset=1):
    state = [int(x) for x in data.split()]
    i = pos = 0
    while True:
        try:
            offset = state[pos]
        except IndexError:
            part_a.final_state = state
            return i
        i += 1
        state[pos] += b_offset if offset >= 3 else 1
        pos += offset


def part_b(data):
    return part_a(data, b_offset=-1)


print("answer_a:", part_a(data))
print("answer_b:", part_b(data))
