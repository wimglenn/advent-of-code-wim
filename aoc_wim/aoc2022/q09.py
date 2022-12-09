"""
--- Day 9: Rope Bridge ---
https://adventofcode.com/2022/day/9
"""
from aocd import data


def cmp(x, y):
    return (x > y) - (x < y)


def dT(H, T):
    dz = H - T
    if abs(dz.imag) > 1 or abs(dz.real) > 1:
        T += cmp(dz.real, 0) + 1j * cmp(dz.imag, 0)
    return T


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
                zs[i] = dT(*zs[i - 1:i + 1])
            seen.add(zs[-1])
    print(f"part {part}:", len(seen))
