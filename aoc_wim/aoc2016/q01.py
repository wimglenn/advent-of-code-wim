import numpy as np
from aocd import data


turn_left = np.array([[0, -1], [1, 0]], dtype=int)  # pi/2 counter-clockwise rotation
turn_right = turn_left @ turn_left @ turn_left  # 3*pi/2 counter-clockwise rotation

turns = {
    "L": turn_left,
    "R": turn_right,
}


def part_a(data):
    position = np.array([0, 0], dtype=int)
    bearing = np.array([0, 1], dtype=int)  # north
    for step in data.split(", "):
        turn, n_blocks = turns[step[0]], int(step[1:])
        bearing = turn @ bearing
        for block in range(n_blocks):
            position += bearing
    return abs(position).sum()


def part_b(data):
    position = np.array([0, 0], dtype=int)
    bearing = np.array([0, 1], dtype=int)  # north
    seen = {(0, 0)}
    for step in data.split(", "):
        turn, n_blocks = turns[step[0]], int(step[1:])
        bearing = turn @ bearing
        for block in range(n_blocks):
            position += bearing
            if tuple(position) in seen:
                return abs(position).sum()
            seen.add(tuple(position))


tests = {
    "R2, L3": 5,
    "R2, R2, R2": 2,
    "R5, L5, R5, R3": 12,
}
for test_data, expected in tests.items():
    assert part_a(test_data) == expected

assert part_b("R8, R4, R4, R8") == 4


print("part a:", part_a(data))
print("part b:", part_b(data))
