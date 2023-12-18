"""
--- Day 18: Lavaduct Lagoon ---
https://adventofcode.com/2023/day/18
"""
from aocd import data

dzs = dict(zip("RDLU0123", (1, 1j, -1, -1j)*2))
za = zb = 0
zas = [za]
zbs = [zb]
for line in data.splitlines():
    d, n, c = line.replace("(#", "0x").rstrip(")").split()
    za += dzs[d] * int(n)
    zb += dzs[c[-1]] * int(c[:-1], 0)
    zas.append(za)
    zbs.append(zb)


def area(zs):
    # Shoelace formula + Pick's theorem
    a = p = 0
    for z0, z1 in zip(zs, zs[1:] + [zs[0]]):
        a += (z1.real + z0.real) * (z1.imag - z0.imag)
        p += abs(z1 - z0)
    return int(a/2 + p/2 + 1)


print("answer_a:", area(zas))
print("answer_b:", area(zbs))
