from aoc_wim.stuff import rsubset_sum
from aoc_wim.stuff import subset_sum

from aoc_wim.aoc2015 import q17


vals = [20, 15, 10, 5, 5]


def test_recursive_implementation():
    assert q17.part_a(vals, target=25, impl=rsubset_sum) == 4
    assert q17.part_b(vals, target=25, impl=rsubset_sum) == 3


def test_dynamic_programming_implementation():
    assert q17.part_a(vals, target=25, impl=subset_sum) == 4
    assert q17.part_b(vals, target=25, impl=subset_sum) == 3
