from aocd import data


z = 0
dz = -1j
seen = {z}
turns = {"R": 1j, "L": -1j}
b = None
for step in data.split(", "):
    turn, n_blocks = step[0], int(step[1:])
    dz *= turns[turn]
    for block in range(n_blocks):
        z += dz
        if b is None and z in seen:
            b = int(abs(z.real) + abs(z.imag))
        seen.add(z)

print("part a:", int(abs(z.real) + abs(z.imag)))
print("part b:", b)
