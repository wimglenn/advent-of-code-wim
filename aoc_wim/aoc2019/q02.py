from aocd import data


def compute(A, noun_verb=None):
    if noun_verb is not None:
        A[1:3] = noun_verb
    i = 0
    while A[i] != 99:
        opcode = A[i]
        if opcode == 1:
            val = A[A[i + 1]] + A[A[i + 2]]
        elif opcode == 2:
            val = A[A[i + 1]] * A[A[i + 2]]
        else:
            raise NotImplementedError
        A[A[i + 3]] = val
        i += 4
    return A


def part_a(data, r1=None, r2=None):
    reg = [int(n) for n in data.split(",")]
    if r1 is not None:
        reg[1] = r1
    if r2 is not None:
        reg[2] = r2
    result = compute(reg)
    return result[0]


def part_b(data):
    target = 19690720
    for r1 in range(100):
        for r2 in range(100):
            if part_a(data, r1, r2) == target:
                return 100 * r1 + r2


tests = {
    "1,9,10,3,2,3,11,0,99,30,40,50": 3500,
    "1,0,0,0,99": 2,
    "2,3,0,3,99": 2,
    "2,4,4,5,99,0": 2,
    "1,1,1,4,99,5,6,0,99": 30,
}

for code, reg0 in tests.items():
    assert part_a(code) == reg0

print(part_a(data, r1=12, r2=2))
print(part_b(data))
