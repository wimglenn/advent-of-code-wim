from aoc_wim.aoc2019 import q16


def test_small_example():
    assert q16.part_a("12345678", 1) == "48226158"
    assert q16.part_a("12345678", 2) == "34040438"
    assert q16.part_a("12345678", 3) == "03415518"
    assert q16.part_a("12345678", 4) == "01029498"
