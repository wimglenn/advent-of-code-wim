"""
--- Day 3: Spiral Memory ---
https://adventofcode.com/2017/day/3
"""
from aocd import data
from aoc_wim.zgrid import manhattan_distance


def gen():
    # yields pairs of (manhattan distance from origin, sum of neighbours)
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
                yield manhattan_distance(pos), sums[pos]


def part_ab(data):
    n = int(data)
    a = b = None
    for i, (distance, sum_) in enumerate(gen(), 1):
        if i == n:
            a = a or distance
        if sum_ > n:
            b = b or sum_
        if a is not None and b is not None:
            return a, b


if __name__ == "__main__":
    a, b = part_ab(data)
    print("part a:", a)
    print("part b:", b)
