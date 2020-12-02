import pytest
from aoc_wim.aoc2017.q22 import mutate


test_data = """\
..#
#..
...
"""


@pytest.mark.parametrize("n,expected,part", [
    (7, 5, "a"),
    (70, 41, "a"),
    (10000, 5587, "a"),
    (100, 26, "b"),
    (10000000, 2511944, "b")
], ids=["a_short", "a_medium", "a_long", "b_medium", "b_long_slow"])
def test_virus_mutation(n, expected, part):
    assert mutate(test_data, n_iterations=n, part=part) == expected
