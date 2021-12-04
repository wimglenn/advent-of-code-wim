"""
--- Day 4: Giant Squid ---
https://adventofcode.com/2021/day/4
"""
from aocd import data
import numpy as np

draw, *boards = data.split("\n\n")
draw = [int(n) for n in draw.split(",")]
boards = [np.array([[int(n) for n in ns.split()] for ns in b.splitlines()]) for b in boards]


def winner_score(draw, boards):
    # removes the winner's board from the game, and return their score
    for i, n in enumerate(draw):
        for board in boards:
            board[board == n] = -1
            if i < 5:
                # nobody can have a bingo with fewer than 5 numbers called
                continue
            if (board.sum(axis=0) == -5).any() or (board.sum(axis=1) == -5).any():
                board[board == -1] = 0
                boards[:] = [b for b in boards if b is not board]
                return board.sum() * n


print("part a:", winner_score(draw, boards))
while boards:
    b = winner_score(draw, boards)
print("part b:", b)
