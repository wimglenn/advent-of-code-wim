import numpy as np

data = 'R3, L2, L2, R4, L1, R2, R3, R4, L2, R4, L2, L5, L1, R5, R2, R2, L1, R4, R1, L5, L3, R4, R3, R1, L1, L5, L4, L2, R5, L3, L4, R3, R1, L3, R1, L3, R3, L4, R2, R5, L190, R2, L3, R47, R4, L3, R78, L1, R3, R190, R4, L3, R4, R2, R5, R3, R4, R3, L1, L4, R3, L4, R1, L4, L5, R3, L3, L4, R1, R2, L4, L3, R3, R3, L2, L5, R1, L4, L1, R5, L5, R1, R5, L4, R2, L2, R1, L5, L4, R4, R4, R3, R2, R3, L1, R4, R5, L2, L5, L4, L1, R4, L4, R4, L4, R1, R5, L1, R1, L5, R5, R1, R1, L3, L1, R4, L1, L4, L4, L3, R1, R4, R1, R1, R2, L5, L2, R4, L1, R3, L5, L2, R5, L4, R5, L5, R3, R4, L3, L3, L2, R2, L5, L5, R3, R4, R3, R4, R3, R1'

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
