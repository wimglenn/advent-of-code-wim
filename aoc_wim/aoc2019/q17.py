from aocd import data
from aoc_wim.aoc2019 import IntComputer
from aoc_wim.stuff import dump_grid
from bidict import bidict


comp = IntComputer(data)
comp.run()

grid = {}
z = 0
dzs = bidict(zip("^>v<", [-1j, 1, 1j, -1]))
for ascii_ord in reversed(comp.output):
    txt = chr(ascii_ord)
    if txt == "\n":
        z += 1j - z.real
        continue
    grid[z] = txt
    if txt in dzs:
        z0 = z
        dz0 = dzs[txt]
    z += 1

dump_grid(grid)

calibration = 0
for z, txt in grid.items():
    if txt == "#" and {grid.get(z + dz) for dz in dzs.inv} == {"#"}:
        calibration += int(z.real) * int(z.imag)
print("part a", calibration)

path = "A,B,A,C,A,B,C,B,C,B\n"
A = "R,10,R,10,R,6,R,4\n"
B = "R,10,R,10,L,4\n"
C = "R,4,L,4,L,10,L,10\n"
display = "n\n"
comp = IntComputer(data)
comp.reg[0] = 2
for char in path + A + B + C + display:
    comp.input.appendleft(ord(char))
comp.run()
print("part b", comp.output[0])
