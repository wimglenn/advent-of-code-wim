import pytest
from parse import parse


expected = """\
House 1 got 10 presents.
House 2 got 30 presents.
House 3 got 40 presents.
House 4 got 70 presents.
House 5 got 60 presents.
House 6 got 120 presents.
House 7 got 80 presents.
House 8 got 150 presents.
House 9 got 130 presents."""


@pytest.mark.parametrize("line", expected.splitlines())
def test_first_nine_houses_on_the_street_slow(line):
    from aoc_wim.aoc2015 import q20  # inline import because the module is slow to load
    i, n = parse("House {:d} got {:d} presents.", line).fixed
    assert q20.A[i] == n
