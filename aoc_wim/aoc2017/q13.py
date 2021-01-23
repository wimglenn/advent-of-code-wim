"""
--- Day 13: Packet Scanners ---
https://adventofcode.com/2017/day/13
"""
from aocd import data


depth2range = dict(map(int, line.split(":")) for line in data.splitlines())
print("part a:", sum(d * r for d, r in depth2range.items() if d % (2 * r - 2) == 0))

t = 0
while not all((d + t) % (2 * r - 2) for d, r in depth2range.items()):
    t += 1
print("part b:", t)
