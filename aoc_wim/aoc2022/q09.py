"""
--- Day 9: Rope Bridge ---
https://adventofcode.com/2022/day/9
"""
from aocd import data


def cmp(x, y):
    return (x > y) - (x < y)


def T1(H, T0):
    dz = H - T0
    if abs(dz.imag) > 1 or abs(dz.real) > 1:
        T0 += complex(cmp(dz.real, 0), cmp(dz.imag, 0))
    return T0


dHs = dict(zip("UDLR", (-1j, 1j, -1, 1)))
for part in "ab":
    L = 2 if part == "a" else 10
    Ts = [0] * L
    seen = set()
    for line in data.splitlines():
        dH, n = line.split()
        for _ in range(int(n)):
            Ts[0] += dHs[dH]
            for i in range(1, L):
                H = Ts[i-1]
                T = Ts[i]
                Ts[i] = T1(H, T)
            seen.add(Ts[-1])
    print(f"part {part}:", len(seen))
