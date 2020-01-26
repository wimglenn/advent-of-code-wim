from collections import deque

from aocd import data


def get_marker(iterator):
    marker = ""
    for i, c in iterator:
        if c == ")":
            break
        marker += c
    duration, multiplier = [int(n) for n in marker.split("x")]
    length = len(marker) + 2
    return [duration, multiplier, length]


def can_parse_marker(data, pos):
    end = data.find(")", pos)
    if end == "-1":
        return False
    assert data[pos] == "("
    assert data[end] == ")"
    substring = data[pos + 1:end]
    if substring.count("x") != 1:
        return False
    left, right = substring.split("x")
    result = left.isdigit() and right.isdigit()
    return result


def part_a(data):
    result = 0
    iterator = enumerate(data)
    for i, c in iterator:
        if c == "(" and can_parse_marker(data, i):
            duration, multiplier, _length = get_marker(iterator)
            try:
                for _ in range(duration):
                    next(iterator)
                    result += multiplier
            except StopIteration:
                break
        else:
            result += 1
    return result


def parsed(data):
    d = deque()
    iterator = enumerate(data)
    while True:
        try:
            i, letter = next(iterator)
        except StopIteration:
            break
        if letter == "(" and can_parse_marker(data, i):
            d.append(get_marker(iterator))
        else:
            d.append(1)
    return d


def part_b(data):
    d = parsed(data)
    result = 0
    while True:
        try:
            x = d.popleft()
        except IndexError:
            break
        if isinstance(x, int):
            result += x
        else:
            duration, multiplier, length = x
            i = 0
            while duration > 0 and i < len(d):
                if isinstance(d[i], int):
                    duration -= 1
                    d[i] *= multiplier
                else:
                    duration -= d[i][2]
                i += 1
    return result


print("part a:", part_a(data))
print("part b:", part_b(data))
