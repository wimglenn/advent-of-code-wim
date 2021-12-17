"""
--- Day 4: Giant Squid ---
https://adventofcode.com/2021/day/4
"""
from aocd import data

draw, *boards = data.split("\n\n")
draw = [int(n) for n in draw.split(",")]
rows = [[[int(n) for n in ns.split()] for ns in b.splitlines()] for b in boards]
cols = [[*zip(*r)] for r in rows]
boards = [[set(r) for r in rs] + [set(c) for c in cs] for rs, cs in zip(rows, cols)]


def winner_score(draw, boards):
    # removes the winner's board from the game, and return their score
    for n in draw:
        for board in boards:
            for line in board:
                line.discard(n)
                if not line:  # this board got bingo
                    remaining_numbers = line.union(*board) - {n}
                    boards[:] = [b for b in boards if b is not board]
                    return sum(remaining_numbers) * n


print("part a:", winner_score(draw, boards))
while boards:
    b = winner_score(draw, boards)
print("part b:", b)
