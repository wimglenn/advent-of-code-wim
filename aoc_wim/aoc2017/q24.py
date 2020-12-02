"""
--- Day 24: Electromagnetic Moat ---
https://adventofcode.com/2017/day/24
"""
from aocd import data


def extend(bridge, segments):
    *rest, (connected, free) = bridge
    end = True
    for i, segment in enumerate(segments):
        if free in segment:
            end = False
            next_segments = segments[:i] + segments[i + 1 :]
            next_bridge = bridge + [(free, segment[segment[0] == free])]
            yield from extend(next_bridge, next_segments)
    if end:
        yield bridge


segments = [tuple(int(x) for x in line.split("/")) for line in data.splitlines()]
bridges = list(extend([(0, 0)], segments))
lengths = [len(b) for b in bridges]
strengths = [sum(x + y for x, y in b) for b in bridges]
longest = max(lengths)
long_indices = [i for i, length in enumerate(lengths) if length == longest]

print("part a:", max(strengths))
print("part b:", max([strengths[i] for i in long_indices]))
