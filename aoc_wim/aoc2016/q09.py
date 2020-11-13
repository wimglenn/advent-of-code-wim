"""
--- Day 9: Explosives in Cyberspace ---
https://adventofcode.com/2016/day/9
"""
from collections import deque
import re
import logging

from aocd import data


log = logging.getLogger(__name__)


pat = re.compile(r"\((?P<n_chars>[0-9]+)x(?P<n_repeats>[0-9]+)\)")


def safe_to_use_fast_algo(data):
    # checks if all assumptions about the data actually hold before using faster path
    # does every "(" start a valid marker?
    for i, char in enumerate(data):
        if char == "(":
            match = pat.match(data, i)
            if match is None:
                log.debug("%d: '(' didn't start a valid marker", i)
                return False
            n_chars = int(match.group("n_chars"))
            # the substring to be repeated must not exceed the remaining length of data
            if n_chars > len(data) - match.end():
                log.debug("%d: substring to be repeated exceeded end", i)
                return False
            for j in range(match.end(), match.end() + n_chars):
                match_nested = pat.match(data, j)
                if match_nested is None:
                    continue
                assert match_nested.start() < match.end() + n_chars
                assert match_nested.start() == j
                # don't split up other markers when repeating
                if match.end() + n_chars < match_nested.end():
                    log.debug("%d: substring to repeated split another marker", i)
                    return False
                n_chars_nested = int(match_nested.group("n_chars"))
                # Can't copy an inner marker that wants to access data
                # outside of the outer marker's reach
                if match.end() + n_chars < match_nested.end() + n_chars_nested:
                    log.debug("%d: inner marker reaches beyond outer marker range", i)
                    return False
    return True


def parse_marker(d, i=0):
    if len(d) - i < 5:
        # need at least 5 chars to make a valid marker (MxN)
        return
    if d[i] != "(":
        # marker must start with (
        return
    vals = []
    for val in d:
        vals.append(val)
        if val == ")":
            break
    assert vals[0] == "("
    if vals[-1] != ")":
        # marker must end with )
        return
    substring = "".join(vals[1:-1])
    try:
        duration, multiplier = [int(x) for x in substring.split("x")]
    except ValueError:
        # in between ( and ) must be number x number
        return
    width = len(substring) + 2
    assert width >= 5
    return duration, multiplier, width


def unzip_slow(data, part="a"):
    length = 0
    d = deque(data)
    while d:
        marker = parse_marker(d)
        if marker is None:
            d.popleft()
            length += 1
            continue
        duration, multiplier, width = marker
        for _ in range(width):
            d.popleft()
        if part == "a":
            for _ in range(min(duration, len(d))):
                d.popleft()
                length += multiplier
        elif part == "b":
            extend = [d[i] for i in range(min(duration, len(d)))] * (multiplier - 1)
            d.extendleft(reversed(extend))
    return length


def unzip_fast(data, part="a"):
    length = 0
    i = 0
    while True:
        m = pat.search(data, i)
        if m is None:
            length += len(data) - i
            break
        n = int(m.group("n_chars"))
        r = int(m.group("n_repeats"))
        if part == "a":
            length += m.start() - i + n * r
        elif part == "b":
            length += m.start() - i + unzip_fast(data[m.end() : m.end() + n], part) * r
        i = m.end() + n
    return length


if safe_to_use_fast_algo(data):
    print("part a:", unzip_fast(data, part="a"))
    print("part b:", unzip_fast(data, part="b"))
else:
    print("part a:", unzip_slow(data, part="a"))
    print("part b:", unzip_slow(data, part="b"))
