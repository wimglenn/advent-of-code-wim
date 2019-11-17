from aocd import data


def gen():
    pos, delta = 0, 1
    sums = {pos: 1}
    yield pos, sums[pos]
    while True:
        pos += 1 - 1j
        for _ in range(4):
            delta *= 1j
            for _ in range(int(2 * abs(pos.real))):
                pos += delta
                neighbours = (pos + dr + dj for dr in (-1, 0, 1) for dj in (-1j, 0, 1j))
                sums[pos] = sum(sums.get(p, 0) for p in neighbours)
                yield int(abs(pos.real) + abs(pos.imag)), sums[pos]


test_distances = {1: 0, 12: 3, 23: 2, 1024: 31}
test_sums = [
    None,
    1,
    1,
    2,
    4,
    5,
    10,
    11,
    23,
    25,
    26,
    54,
    57,
    59,
    122,
    133,
    142,
    147,
    304,
    330,
    351,
    362,
    747,
    806,
]


def part_ab(data):
    n = int(data)
    a = b = None
    for i, (distance, sum_) in enumerate(gen(), 1):
        try:
            assert test_distances[i] == distance
        except KeyError:
            pass
        try:
            assert test_sums[i] == sum_
        except IndexError:
            pass
        if i == n:
            a = a or distance
        if sum_ > n:
            b = b or sum_
        if a and b:
            return a, b


a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
