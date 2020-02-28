from aoc_wim.aoc2016 import q16


padding = """\
1 becomes 100.
0 becomes 001.
11111 becomes 11111000000.
111100001010 becomes 1111000010100101011110000.
"""


def test_padding():
    for line in padding.splitlines():
        left, right = line.rstrip(".").split(" becomes ")
        assert q16.pad(left, n=len(right)) == right


def test_checksum():
    data = "110010110100"
    assert q16.f(data, n=12) == "100"


def test_len20_disk():
    data = "10000"
    n = 20
    assert q16.f(data, n) == "01100"
