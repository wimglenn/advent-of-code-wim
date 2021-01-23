import pytest
from aoc_wim.aoc2018 import q05


@pytest.mark.parametrize("polymer,reacted", [
    ("aA", ""),
    ("abBA", ""),
    ("abAB", "abAB"),
    ("aabAAB", "aabAAB"),
    ("dabAcCaCBAcCcaDA", "dabCBAcaDA"),
])
def test_example_reactions(polymer, reacted):
    assert q05.react(polymer) == reacted


def test_example_improvements():
    polymer = "dabAcCaCBAcCcaDA"
    results = q05.choices(polymer)
    assert results == {
        "a": "dbCBcD",
        "b": "daCAcaDA",
        "c": "daDA",
        "d": "abCBAc",
    }
