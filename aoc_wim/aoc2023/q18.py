"""
--- Day 18: Lavaduct Lagoon ---
https://adventofcode.com/2023/day/18
"""
from aocd import data

dzs = dict(zip("RDLU", (1, 1j, -1, -1j)))
dzs.update(dict(zip("0123", (1, 1j, -1, -1j))))
za = zb = 0
pa = pb = 0
zas = [za]
zbs = [zb]
for line in data.splitlines():
    d, n, c = line.split()
    c = c.strip("#()")
    dza = dzs[d]
    dzb = dzs[c[-1]]
    na = int(n)
    nb = int(c[:-1], 16)
    za += dza * na
    zb += dzb * nb
    pa += na
    pb += nb
    zas.append(za)
    zbs.append(zb)


def shoelace(zs):
    area = 0
    j = len(zs) - 1
    for i in range(len(zs)):
        area += (zs[j].real + zs[i].real) * (zs[j].imag - zs[i].imag)
        j = i
    return int(abs(area / 2))


print("answer_a:", shoelace(zas) + pa//2 + 1)
print("answer_b:", shoelace(zbs) + pb//2 + 1)
