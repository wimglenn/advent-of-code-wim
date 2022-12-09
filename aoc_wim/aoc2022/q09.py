"""
--- Day 9: Rope Bridge ---
https://adventofcode.com/2022/day/9
"""
from aocd import data


def cmp(x, y):
    return (x > y) - (x < y)


dHs = dict(zip("UDLR", (-1j, 1j, -1, 1)))
seen_a = set()
seen_b = set()
zs = [0] * 10
for line in data.splitlines():
    dH, n = line.split()
    for _ in range(int(n)):
        zs[0] += dHs[dH]
        for i in range(9):
            dz = zs[i] - zs[i + 1]
            if abs(dz) >= 2:
                zs[i + 1] += cmp(dz.real, 0) + 1j * cmp(dz.imag, 0)
        seen_a.add(zs[1])
        seen_b.add(zs[-1])

print("part a:", len(seen_a))
print("part b:", len(seen_b))
