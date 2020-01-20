from aoc_wim.aoc2015 import q11


def test_requirements():
    assert q11.req1("hijklmmn")
    assert not q11.req2("hijklmmn")
    assert q11.req3("abbceffg")
    assert not q11.req1("abbceffg")
    assert not q11.req3("abbcegjk")
