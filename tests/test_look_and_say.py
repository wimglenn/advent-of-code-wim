from aoc_wim.aoc2015.q10 import look_and_say


def test_look_and_say_examples():
    assert look_and_say("211") == "1221"
    assert look_and_say("1", n=1) == "11"
    assert look_and_say("1", n=2) == "21"
    assert look_and_say("1", n=3) == "1211"
    assert look_and_say("1", n=4) == "111221"
    assert look_and_say("1", n=5) == "312211"
