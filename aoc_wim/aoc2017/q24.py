from aocd import data

test_data = """\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
"""


def get_segments(data):
    return [tuple(int(x) for x in line.split("/")) for line in data.splitlines()]


def extend(bridge, segments):
    *rest, (connected, free) = bridge
    end = True
    for i, segment in enumerate(segments):
        if free in segment:
            end = False
            next_segments = segments[:i] + segments[i + 1 :]
            next_bridge = bridge + [(free, segment[segment[0] == free])]
            yield from extend(next_bridge, next_segments)
    if end:
        yield bridge


def strongest_and_longest(data):
    bridges = extend(bridge=[(0, 0)], segments=get_segments(data))
    lengths_and_strengths = [(len(b), sum(x + y for x, y in b)) for b in bridges]
    strength_strongest = max(strength for length, strength in lengths_and_strengths)
    _length_longest, strength_longest = max(lengths_and_strengths)
    return strength_strongest, strength_longest


assert strongest_and_longest(test_data) == (31, 19)
strongest, longest = strongest_and_longest(data)
print(strongest)
print(longest)
