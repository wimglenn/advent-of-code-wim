"""
--- Day 8: Matchsticks ---
https://adventofcode.com/2015/day/8
"""
from aocd import data


def tokens(s):
    iterator = iter(s)
    for char in iterator:
        if char == "\\":
            char += next(iterator)
            if char.endswith("x"):
                char += next(iterator)
                char += next(iterator)
        yield char


def encoder(s):
    iterator = iter(s)
    yield '"'
    for char in iterator:
        if char == '"' or char == "\\":
            yield "\\"
        yield char
    yield '"'


def tokens_len(s):
    return sum(1 for token in tokens(s)) - 2


def length_diff(data):
    return sum(len(line) - tokens_len(line) for line in data.splitlines())


def encoded_diff(data):
    return sum(len("".join(encoder(line))) - len(line) for line in data.splitlines())


print(length_diff(data))
print(encoded_diff(data))
