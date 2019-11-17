import numpy as np
from aocd import data


def part_a(data, roll=1):
    a = np.fromiter(data, dtype=int)
    b = np.roll(a, roll)
    return a[a == b].sum()


def part_b(data):
    return part_a(data, roll=len(data) // 2)


tests_a = {
    "1122": 3,
    "1111": 4,
    "1234": 0,
    "91212129": 9,
}
for test_data, expected in tests_a.items():
    assert part_a(test_data) == expected

tests_b = {
    "1212": 6,
    "1221": 0,
    "123425": 4,
    "123123": 12,
    "12131415": 4,
}
for test_data, expected in tests_b.items():
    assert part_b(test_data) == expected

print("part a:", part_a(data))
print("part b:", part_b(data))
