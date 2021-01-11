"""
--- Day 9: Marble Mania ---
https://adventofcode.com/2018/day/9
"""
from aocd import data
from parse import parse


class Node:

    __slots__ = "val", "left", "right"

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def get_high_score(n_players, n_marbles):
    n = Node(val=0)
    n.left = n.right = n
    scores = [0] * n_players
    for m in range(n_marbles):
        if m % 23 != 22:
            left = n.right
            right = n.right.right
            n = Node(val=m + 1, left=left, right=right)
            left.right = right.left = n
        else:
            n = right = n.left.left.left.left.left.left
            left = n.left.left
            scores[m % n_players] += m + 1 + n.left.val
            left.right = right
            right.left = left
    high_score = max(scores)
    return high_score


template = "{:d} players; last marble is worth {:d} points"
n_players, n_marbles = parse(template, data)
print("part a:", get_high_score(n_players, n_marbles))
print("part b:", get_high_score(n_players, n_marbles * 100))
