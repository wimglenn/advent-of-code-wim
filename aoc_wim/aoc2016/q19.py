"""
--- Day 19: An Elephant Named Joseph ---
https://adventofcode.com/2016/day/19
"""
from collections import deque

from aocd import data


def part_a(n):
    elves = deque(range(1, int(n) + 1))
    while elves:
        elves.rotate(-1)
        elf = elves.popleft()
    return elf


def part_b(n):
    n = int(n)
    elves = deque(range(1, n + 1))
    elves.rotate((n + 1) // 2)
    while elves:
        elf = elves.popleft()
        elves.rotate(n // 2 + n // 2 - 1)
        n -= 1
    return elf


print("part a:", part_a(data))
print("part b:", part_b(data))
