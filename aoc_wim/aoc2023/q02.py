"""
--- Day 2: Cube Conundrum ---
https://adventofcode.com/2023/day/2
"""
from aocd import data

bag = dict(zip("rgb", [12, 13, 14]))
a = b = 0
for line in data.splitlines():
    maxs = dict.fromkeys("rgb", 0)
    g, line = line.split(": ")
    g = int(g.removeprefix("Game "))
    handfuls = line.split("; ")
    game_possible = True
    for handful in handfuls:
        counts = dict.fromkeys("rgb", 0)
        for n_c in handful.split(", "):
            n, c = n_c.split()
            counts[c[0]] += int(n)
        for c in "rgb":
            maxs[c] = max(maxs[c], counts[c])
        if any(counts[c] > bag[c] for c in "rgb"):
            game_possible = False
    a += g * game_possible
    b += maxs["r"] * maxs["g"] * maxs["b"]

print("answer_a:", a)
print("answer_b:", b)
