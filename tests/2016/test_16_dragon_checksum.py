from aoc_wim.aoc2016 import q16


padding = """\
1 becomes 100.
0 becomes 001.
11111 becomes 11111000000.
111100001010 becomes 1111000010100101011110000.
10000 becomes 10000011110.
10000011110 becomes 10000011110010000111110.
"""


def test_padding():
    for line in padding.splitlines():
        left, right = line.rstrip(".").split(" becomes ")
        assert q16.pad(left, n=len(right)) == right
