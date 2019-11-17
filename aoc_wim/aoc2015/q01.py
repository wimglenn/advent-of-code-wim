from aocd import data


def part_ab(data):
    direction = {"(": +1, ")": -1}
    basement = None
    floor = 0
    for i, c in enumerate(data, 1):
        floor += direction[c]
        if basement is None and floor == -1:
            basement = i
    return floor, basement


a_tests = {
    "(())": 0,
    "()()": 0,
    "(((": 3,
    "(()(()(": 3,
    "))(((((": 3,
    "())": -1,
    "))(": -1,
    ")))": -3,
    ")())())": -3,
}
for test_data, expected in a_tests.items():
    assert part_ab(test_data)[0] == expected


b_tests = {
    ")": 1,
    "()())": 5,
}
for test_data, expected in b_tests.items():
    assert part_ab(test_data)[1] == expected


a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
