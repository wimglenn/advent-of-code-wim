from functools import reduce
from operator import xor

from aocd import data


def munge(state, lengths, n=256, iterations=64):
    skip_size = 0
    current_position = 0
    for i in range(iterations):
        for length in lengths:
            for i in range(length // 2):
                i1 = (current_position + i) % n
                i2 = (current_position + length - i - 1) % n
                state[i1], state[i2] = state[i2], state[i1]
            current_position += length + skip_size
            skip_size += 1


def part_a(data, n=256):
    lengths = [int(x) for x in data.split(",")]
    state = list(range(n))
    munge(state, lengths=lengths, n=n, iterations=1)
    return state[0] * state[1]


def knot_hash(data, n=256):
    state = list(range(n))
    lengths = [ord(x) for x in data] + [17, 31, 73, 47, 23]
    munge(state, lengths, n)
    reduced = [reduce(xor, state[16 * i : 16 * (i + 1)]) for i in range(16)]
    return bytes(reduced).hex()


test_a = "3,4,1,5"
assert part_a(test_a, n=5) == 12

tests_b = {
    "": "a2582a3a0e66e6e86e3812dcb672a272",
    "AoC 2017": "33efeb34ea91902bb2f59c9920caa6cd",
    "1,2,3": "3efbe78a8d82f29979031a4aa0b16a9d",
    "1,2,4": "63960835bcdc130f0b66d7ff4f6a5a8e",
}
for k, v in tests_b.items():
    assert knot_hash(k) == v


if __name__ == "__main__":
    print("part a:", part_a(data))
    print(knot_hash(data))
