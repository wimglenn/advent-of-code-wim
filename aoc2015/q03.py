from aocd import data


step = {
    '^': 1j,
    '>': 1,
    'v': -1j,
    '<': -1,
}

pos = 0
seen = {pos}

for c in data:
    pos += step[c]
    seen |= {pos}

print(len(seen))

pos = 0
seen = {pos}

for c in data[0::2]:  # santa
    pos += step[c]
    seen |= {pos}

pos = 0
for c in data[1::2]:  # robo-santa
    pos += step[c]
    seen |= {pos}

print(len(seen))
