from aoc_wim.aoc2017 import q21

rules = """\
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
"""


def test_fractal_evolution():
    assert q21.evolve(rules, 2) == 12
