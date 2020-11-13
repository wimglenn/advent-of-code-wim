from aoc_wim.aoc2017.q03 import gen

example_sums = [
    1,
    1,
    2,
    4,
    5,
    10,
    11,
    23,
    25,
    26,
    54,
    57,
    59,
    122,
    133,
    142,
    147,
    304,
    330,
    351,
    362,
    747,
    806,
]


def test_example_spiral():
    g = gen()
    actual = [next(g)[1] for _ in example_sums]
    assert actual == example_sums
