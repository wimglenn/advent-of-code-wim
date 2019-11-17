from aocd import data


step = {
    "^": 1j,
    ">": 1,
    "v": -1j,
    "<": -1,
}


def part_a(data):
    pos = 0
    seen = {pos}

    for c in data:
        pos += step[c]
        seen |= {pos}

    return len(seen)


def part_b(data):
    pos = 0
    seen = {pos}

    for c in data[0::2]:  # santa
        pos += step[c]
        seen |= {pos}

    pos = 0
    for c in data[1::2]:  # robo-santa
        pos += step[c]
        seen |= {pos}

    return len(seen)


a_tests = {
    ">": 2,
    "^>v<": 4,
    "^v^v^v^v^v": 2,
}
for test_data, expected in a_tests.items():
    assert part_a(test_data) == expected

b_tests = {
    "^v": 3,
    "^>v<": 3,
    "^v^v^v^v^v": 11,
}
for test_data, expected in b_tests.items():
    assert part_b(test_data) == expected


print("part a:", part_a(data))
print("part b:", part_b(data))
