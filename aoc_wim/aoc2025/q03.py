"""
--- Day 3: Lobby ---
https://adventofcode.com/2025/day/3
"""

from aocd import data


def max_jolts(line, d=2):
    s = []
    i = 0
    while d:
        m = max(line[i : 1 - d or None])
        s.append(m)
        i = line.index(m, i) + 1
        d -= 1
    return int("".join(s))


lines = data.split()
print("answer_a:", sum(max_jolts(x, d=2) for x in lines))
print("answer_b:", sum(max_jolts(x, d=12) for x in lines))
