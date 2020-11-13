import pytest

from aoc_wim.aoc2017 import q10


def test_munge_example():
    assert q10.part_a("3,4,1,5", n=5) == 12


@pytest.mark.parametrize("data,expected", [
    ("", "a2582a3a0e66e6e86e3812dcb672a272"),
    ("AoC 2017", "33efeb34ea91902bb2f59c9920caa6cd"),
    ("1,2,3", "3efbe78a8d82f29979031a4aa0b16a9d"),
    ("1,2,4", "63960835bcdc130f0b66d7ff4f6a5a8e"),
])
def test_knot_hash(data, expected):
    assert q10.knot_hash(data) == expected
