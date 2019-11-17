from collections import deque

from aocd import data


def part_a(n):
    elves = deque(range(1, int(n) + 1))
    while elves:
        elves.rotate(-1)
        elf = elves.popleft()
    return elf


def part_b(n):
    n = int(n)
    elves = deque(range(1, n + 1))
    elves.rotate((n + 1) // 2)
    while elves:
        elf = elves.popleft()
        elves.rotate(n // 2 + n // 2 - 1)
        n -= 1
    return elf


assert part_a(5) == 3
assert part_b(5) == 2

print("part a:", part_a(data))
print("part b:", part_b(data))
