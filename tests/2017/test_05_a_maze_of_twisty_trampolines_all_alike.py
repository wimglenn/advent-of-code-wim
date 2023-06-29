from aoc_wim.aoc2017 import q05


def test_final_state_a():
    q05.part_a("0 3 0 1 -3")
    assert q05.part_a.final_state == [2, 5, 0, 1, -2]


def test_final_state_b():
    q05.part_b("0 3 0 1 -3")
    assert q05.part_a.final_state == [2, 3, 2, 3, -1]
