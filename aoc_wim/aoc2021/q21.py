"""
--- Day 21: Dirac Dice ---
https://adventofcode.com/2021/day/21
"""
from aocd import data
from collections import Counter


def play_deterministic(p1, p2):
    pos = [p1, p2]
    score = [0, 0]
    rolls = 0
    while True:
        for i in 0, 1:
            rolls += 3
            pos[i] += 3 * (rolls - 1)
            pos[i] = (pos[i] - 1) % 10 + 1
            score[i] += pos[i]
            if score[i] >= 1000:
                return rolls * score[i - 1]


def wins(p1, p2, s1, s2, memo, rolls):
    if s2 >= 21:
        return 0, 1
    if (p1, p2, s1, s2) not in memo:
        t1 = t2 = 0
        for roll, count in rolls.items():
            next_p1 = (p1 + roll - 1) % 10 + 1
            wins2, wins1 = wins(p2, next_p1, s2, s1 + next_p1, memo, rolls)
            t1 += wins1 * count
            t2 += wins2 * count
        memo[p1, p2, s1, s2] = t1, t2
    return memo[p1, p2, s1, s2]


def play_quantum(p1, p2):
    r = [1, 2, 3]
    rolls = Counter([r1 + r2 + r3 for r1 in r for r2 in r for r3 in r])
    wins1, wins2 = wins(p1, p2, 0, 0, {}, rolls)
    return max(wins1, wins2)


p1, p2 = [int(line.split()[-1]) for line in data.splitlines()]
print("part a:", play_deterministic(p1, p2))
print("part b:", play_quantum(p1, p2))
