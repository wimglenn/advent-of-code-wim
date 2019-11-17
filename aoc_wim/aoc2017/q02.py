from itertools import combinations

from aocd import data

test_a = """5 1 9 5
7 5 3
2 4 6 8
"""


def part_a(data):
    result = 0
    for line in data.splitlines():
        row = [int(x) for x in line.split()]
        result += max(row) - min(row)
    return result


test_b = """5 9 2 8
9 4 7 3
3 8 6 5"""


def part_b(data):
    result = 0
    for line in data.splitlines():
        row = [int(x) for x in line.split()]
        for x, y in combinations(row, 2):
            denominator, numerator = sorted([x, y])
            quotient, remainder = divmod(numerator, denominator)
            if not remainder:
                result += quotient
                break
    return result


assert part_a(test_a) == 18
assert part_b(test_b) == 9

print("part a:", part_a(data))
print("part b:", part_b(data))
