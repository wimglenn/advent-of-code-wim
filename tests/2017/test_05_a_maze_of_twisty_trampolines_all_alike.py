from aoc_wim.aoc2017 import q05


test_data = "0 3 0 1 -3"


def test_state_a():
    q05.part_a(test_data)
    assert q05.part_a.final_state == [2, 5, 0, 1, -2]


def test_state_b():
    q05.part_b(test_data)
    assert q05.part_a.final_state == [2, 3, 2, 3, -1]
