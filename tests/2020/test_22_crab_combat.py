from collections import deque

from aoc_wim.aoc2020 import q22

# Here is an example of a small game that would loop forever without the
# infinite game prevention rule:

test_data = """\
Player 1:
43
19

Player 2:
2
29
14
"""


def test_infinite_recursion_rule():
    data1, data2 = test_data.split("\n\n")
    cards1 = [int(x) for x in data1.splitlines()[1:]]
    cards2 = [int(x) for x in data2.splitlines()[1:]]
    p1a = deque(cards1)
    p2a = deque(cards2)
    winner = q22.play(p1a, p2a, part="b")
    assert winner == 1
