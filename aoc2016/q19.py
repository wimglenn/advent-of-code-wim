from aocd import data
from collections import deque


def part_a(n):
    elves = deque(range(1, int(n)+1))
    while elves:
        elves.rotate(-1)
        elf = elves.popleft()
    return elf


def part_b(n):
    n = int(n)
    elves = deque(range(1, n+1))
    while elves:
        elves.rotate(-(n//2))
        elf = elves.popleft()
        elves.rotate(n//2 - 1)
        n -= 1
    return elf


assert part_a(5) == 3
assert part_b(5) == 2

assert part_a(9) == 3
assert part_b(9) == 9

assert part_a(10) == 5
assert part_b(10) == 1

assert part_a(27) == 23
assert part_b(27) == 27

assert part_a(81) == 35
assert part_b(81) == 81

assert part_a(243) == 231
assert part_b(243) == 243

assert part_a(98) == 69
assert part_b(98) == 17

assert part_a(99) == 71
assert part_b(99) == 18

assert part_a(100) == 73
assert part_b(100) == 19

assert part_a(101) == 75
assert part_b(101) == 20

print(part_a(data))
# print(part_b(data))
