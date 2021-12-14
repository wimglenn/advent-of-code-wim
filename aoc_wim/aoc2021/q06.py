"""
--- Day 6: Lanternfish ---
https://adventofcode.com/2021/day/6
"""
from aocd import data


def rotate(fish, n=1):
    for _ in range(n):
        fish[:] = fish[1:] + fish[:1]
        fish[6] += fish[-1]
    return sum(fish)


fish = [data.count(f) for f in "012345678"]
print("part a:", rotate(fish, n=80))
print("part b:", rotate(fish, n=256-80))
