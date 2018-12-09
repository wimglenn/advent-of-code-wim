from  aocd import data
from parse import parse
from collections import deque, defaultdict


def get_high_score(n_players, n_marbles):
    scores = defaultdict(int)
    d = deque([0])
    current_marble = 0
    current_player = 0
    pos = 0
    for n in range(1, n_marbles + 1):
        pos += 2
        pos %= len(d)
        current_marble += 1
        d.insert(pos, current_marble)
        current_player += 1
        if current_player > n_players:
            current_player = 1
        if current_marble % 23 == 0:
            scores[current_player] += d[pos]
            del d[pos]
            pos = (pos - 9) % len(d)
            scores[current_player] += d[pos]
            del d[pos]
    high_score = max(scores.values())
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
n_players, n_marbles = parse(template, data)
part_a = get_high_score(n_players, n_marbles)
print(part_a)  # 386151

# part_b = get_high_score(n_players, n_marbles*100)
# print(part_b)  #
