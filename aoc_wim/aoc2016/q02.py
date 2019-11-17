from aocd import data


directions = {"U": 1j, "D": -1j, "L": -1, "R": 1}
grid1 = [
    -1 + 1j,
    1j,
    1 + 1j,
    -1,
    0,
    1,
    -1 - 1j,
    -1j,
    1 - 1j,
]
keypad1 = {k: str(v) for v, k in enumerate(grid1, 1)}

keypad2 = {
    2j: "1",
    -1 + 1j: "2",
    1j: "3",
    1 + 1j: "4",
    -2: "5",
    -1: "6",
    0: "7",
    1: "8",
    2: "9",
    -1 - 1j: "A",
    -1j: "B",
    1 - 1j: "C",
    -2j: "D",
}


def decode(keypad, data, pos0):
    pos = pos0
    code = ""
    for line in data.splitlines():
        for step in line:
            step = directions[step]
            if pos + step in keypad:
                pos += step
        code += keypad[pos]
    return code


def part_a(data):
    return decode(keypad1, data, pos0=0)


def part_b(data):
    return decode(keypad2, data, pos0=-2)


test_data = """\
ULL
RRDDD
LURDL
UUUUD"""
assert part_a(test_data) == "1985"
assert part_b(test_data) == "5DB3"

print("part a:", part_a(data))
print("part b:", part_b(data))
