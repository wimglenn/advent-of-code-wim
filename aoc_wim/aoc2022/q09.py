"""
--- Day 9: Rope Bridge ---
https://adventofcode.com/2022/day/9
"""
from aocd import data


def cmp(x, y):
    return (x > y) - (x < y)


dHs = dict(zip("UDLR", (-1j, 1j, -1, 1)))
for part in "ab":
    tail_length = 2 if part == "a" else 10
    zs = [0] * tail_length
    seen = set()
    for line in data.splitlines():
        dH, n = line.split()
        for _ in range(int(n)):
            zs[0] += dHs[dH]
            for i in range(1, tail_length):
                dz = zs[i-1] - zs[i]
                if abs(dz) >= 2:
                    zs[i] += cmp(dz.real, 0) + 1j * cmp(dz.imag, 0)
            seen.add(zs[-1])
    print(f"part {part}:", len(seen))
