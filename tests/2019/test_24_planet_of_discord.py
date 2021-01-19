from aoc_wim.aoc2019 import q24


test_bugs = """\
....#
#..#.
#..##
..#..
#....
"""


def test_example_b():
    result = q24.part_b(test_bugs, t=10)
    assert result == 99
