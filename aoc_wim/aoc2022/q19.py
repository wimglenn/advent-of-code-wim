"""
--- Day 19: Not Enough Minerals ---
https://adventofcode.com/2022/day/19
"""
import math
import re

from aocd import data


lines = data.split("\n\n") if "\n\n" in data else data.splitlines()
bps = []
for line in lines:
    pk, ore3, ore2, ore1, clay, ore0, obs = map(int, re.findall(r"\d+", line))
    bps.append((pk, ore3, ore2, ore1, clay, ore0, obs, max(ore3, ore2, ore1, ore0)))


def search(stack, blueprint):
    _pk, ore3, ore2, ore1, clay, ore0, obs, ore = blueprint
    tri = [t * (t - 1) // 2 for t in range(33)]
    max_geodes = 0
    while stack:
        r, n0, n1, n2, n3, r0, r1, r2, r3, t = stack.pop()
        g = n0 + r0 * t
        if g > max_geodes:
            max_geodes = g
        if t == 1:
            continue  # on the very last minute, building another robot is not useful
        if r == 0 and not r1:
            continue  # you need at least one obsidian robot before considering a geode robot
        elif r == 1 and not r2:
            continue  # you need at least one clay robot before considering an obsidian robot
        if r == 1 and r1 >= obs:
            continue  # don't need any more obsidian than you can actually spend
        elif r == 2 and r2 >= clay:
            continue  # don't need any more clay than you can actually spend
        elif r == 3 and r3 >= ore:
            continue  # don't need any more ore than you can actually spend
        if n0 + t * r0 + tri[t] <= max_geodes:
            continue  # prune this branch - it can't beat our best so far
        if r == 0 and n1 >= obs and n3 >= ore0:  # get a geode robot
            stack += [(r, n0 + r0, n1 + r1 - obs, n2 + r2, n3 + r3 - ore0, r0 + 1, r1, r2, r3, t - 1) for r in range(4)]
        elif r == 1 and n2 >= clay and n3 >= ore1:  # get an obsidian robot
            stack += [(r, n0 + r0, n1 + r1, n2 + r2 - clay, n3 + r3 - ore1, r0, r1 + 1, r2, r3, t - 1) for r in range(4)]
        elif r == 2 and n3 >= ore2:  # get a clay robot
            stack += [(r, n0 + r0, n1 + r1, n2 + r2, n3 + r3 - ore2, r0, r1, r2 + 1, r3, t - 1) for r in range(4)]
        elif r == 3 and n3 >= ore3:  # get an ore robot
            stack += [(r, n0 + r0, n1 + r1, n2 + r2, n3 + r3 - ore3, r0, r1, r2, r3 + 1, t - 1) for r in range(4)]
        else:  # just wait - accumulates more minerals
            stack.append((r, n0 + r0, n1 + r1, n2 + r2, n3 + r3, r0, r1, r2, r3, t - 1))
    print(f"{max_geodes=} {blueprint=}")
    return max_geodes


s0 = 0, 0, 0, 0, 0, 0, 0, 1
print("answer_a:", sum(bp[0] * search([(2, *s0, 24), (3, *s0, 24)], bp) for bp in bps))
print("answer_b:", math.prod(search([(2, *s0, 32), (3, *s0, 32)], bp) for bp in bps[:3]))
