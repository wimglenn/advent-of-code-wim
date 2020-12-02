from aoc_wim.aoc2017 import q16


def test_example_a():
    assert q16.dance(data="s1,x3/4,pe/b", d=list("abcde")) == "baedc"


def test_example_b():
    assert q16.dance(data="s1,x3/4,pe/b", d=list("abcde"), n=2) == "ceadb"
