from aocd import data


directions = {
    "R": 1j ** 0,
    "U": 1j ** 1,
    "L": 1j ** 2,
    "D": 1j ** 3,
}


def solve(data, part="a"):
    wires = data.splitlines()
    seen = []
    for i, wire in enumerate(wires):
        seen.append({})
        pos = d = 0
        for step in wire.split(","):
            direction, distance = directions[step[0]], int(step[1:])
            for _ in range(distance):
                pos += direction
                d += 1
                if pos not in seen[-1]:
                    seen[-1][pos] = d
    crossings = seen[0].keys() & seen[1].keys()
    if part == "a":
        result = min([int(abs(z.real) + abs(z.imag)) for z in crossings])
    else:
        result = min([seen[0][z] + seen[1][z] for z in crossings])
    return result


tests = {
    "R8,U5,L5,D3\nU7,R6,D4,L4": (6, 30,),
    "R75,D30,R83,U83,L12,D49,R71,U7,L72\n"
    "U62,R66,U55,R34,D71,R55,D58,R83": (159, 610,),
    "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n"
    "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7": (135, 410,),
}

for test_data, (a, b) in tests.items():
    assert solve(test_data, part="a") == a
    assert solve(test_data, part="b") == b

print(solve(data, part="a"))
print(solve(data, part="b"))
