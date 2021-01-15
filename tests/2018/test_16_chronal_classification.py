from aoc_wim.aoc2018 import q16

test_data = """\
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
"""


def test_choices():
    assert len(q16.choices(test_data)) == 3
    assert set(q16.choices(test_data)) == {"mulr", "addi", "seti"}
