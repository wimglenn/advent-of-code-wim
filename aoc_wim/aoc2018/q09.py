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


# n_players, n_marbles, high_score
tests = [(9, 25, 32)]

tests_txt = """10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305"""

test_template = "{:d} players; last marble is worth {:d} points: high score is {:d}"

for line in tests_txt.splitlines():
    parsed = parse(test_template, line)
    tests.append(parsed.fixed)

for n_players, n_marbles, high_score in tests:
    assert get_high_score(n_players, n_marbles) == high_score

template = "{:d} players; last marble is worth {:d} points"


def part_a(data):
    n_players, n_marbles = parse(template, data)
    return get_high_score(n_players, n_marbles)


def part_b(data):
    n_players, n_marbles = parse(template, data)
    return get_high_score(n_players, n_marbles * 100)


print("part a:", part_a(data))
print("part b:", part_b(data))
