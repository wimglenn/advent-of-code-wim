from itertools import cycle

from aocd import data


def part_a(data):
    return sum([int(x) for x in data.split()])


def part_b(data):
    f = 0
    seen = {f}
    for n in cycle([int(x) for x in data.split()]):
        f += n
        if f in seen:
            return f
        seen |= {f}


a_tests = {"+1 -2 +3 +1": 3, "+1 +1 +1": 3, "+1 +1 -2": 0, "-1 -2 -3": -6}
for test_data, result in a_tests.items():
    assert part_a(test_data) == result

b_tests = {
    "+1 -2 +3 +1": 2,
    "+1 -1": 0,
    "+3 +3 +4 -2 -4": 10,
    "-6 +3 +8 +5 -6": 5,
    "+7 +7 -2 -7 -4": 14,
}
for test_data, result in b_tests.items():
    assert part_b(test_data) == result


print("part a:", part_a(data))
print("part b:", part_b(data))
