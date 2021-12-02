from aocd import data
from aoc_wim.zgrid import ZGrid

aim = za = zb = 0
for line in data.splitlines():
    direction, X = line.split()
    X = int(X)
    dz = ZGrid.dzs[direction]
    za += dz * X
    if direction == "forward":
        zb += X + aim * X
    else:
        aim += dz * X

print("part a:", int(za.real) * int(za.imag))
print("part b:", int(zb.real) * int(zb.imag))
