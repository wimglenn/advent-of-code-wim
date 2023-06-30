from aoc_wim.aoc2016 import q17


def test_no_path():
    assert q17.bfs("hijkl", part="a") is None
    assert q17.bfs("hijkl", part="b") is None
