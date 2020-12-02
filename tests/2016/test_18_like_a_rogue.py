from aoc_wim.aoc2016 import q18

test_grid_small = """\
..^^.
.^^^^
^^..^
"""

test_grid_medium = """\
.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^
"""


def test_small_grid_generation():
    assert q18.make_grid("..^^.", nrows=3) == test_grid_small


def test_medium_grid_generation():
    assert q18.make_grid(".^^.^.^^^^", nrows=10) == test_grid_medium


def test_n_safe_tiles():
    assert q18.n_safe_tiles(".^^.^.^^^^", nrows=10) == 38
