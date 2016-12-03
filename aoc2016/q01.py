from aocd import data
import numpy as np


position = np.array([0, 0], dtype=int)
bearing = np.array([0, 1], dtype=int)  # north

turn_left = np.array([[0, -1], [1, 0]], dtype=int)  # pi/2 counter-clockwise rotation
turn_right = turn_left @ turn_left @ turn_left  # 3*pi/2 counter-clockwise rotation

turns = {
    'L': turn_left,
    'R': turn_right,
}

seen = {(0, 0)}
seen_twice = None

for step in data.split(', '):
    turn, n_blocks = turns[step[0]], int(step[1:])
    bearing = turn @ bearing
    for block in range(n_blocks):
        position += bearing
        if seen_twice is None and tuple(position) in seen:
            seen_twice = tuple(position)
        seen.add(tuple(position))

print(position.sum())
print(sum(seen_twice))
