"""
--- Day 22: Crab Combat ---
https://adventofcode.com/2020/day/22
"""
from aocd import data
from collections import deque
from itertools import islice


def play(p1, p2, part="a"):
    seen = set()
    while p1 and p2:
        if part == "b":
            k = *p1, None, *p2
            if k in seen:
                return 1
            seen.add(k)
        c1 = p1.popleft()
        c2 = p2.popleft()
        if part == "b" and c1 <= len(p1) and c2 <= len(p2):
            p1r = deque(islice(p1, 0, c1))
            p2r = deque(islice(p2, 0, c2))
            winner = play(p1r, p2r, part)
        else:
            winner = 1 if c1 > c2 else 2
        if winner == 1:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)
    return winner


def score(hand):
    return sum(i * n for i, n in enumerate(reversed(hand), start=1))


if __name__ == "__main__":
    data1, data2 = data.split("\n\n")
    cards1 = [int(x) for x in data1.splitlines()[1:]]
    cards2 = [int(x) for x in data2.splitlines()[1:]]

    p1a = deque(cards1)
    p2a = deque(cards2)
    play(p1a, p2a)
    print("part a:", score(p1a or p2a))

    p1b = deque(cards1)
    p2b = deque(cards2)
    play(p1b, p2b, part="b")
    print("part b:", score(p1b or p2b))
