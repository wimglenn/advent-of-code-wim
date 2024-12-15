"""
--- Day 15: Warehouse Woes ---
https://adventofcode.com/2024/day/15
"""
from aocd import data
from aoc_wim.zgrid import ZGrid


warehouse, path = data.split("\n\n")
grid = ZGrid(warehouse)
dzs = [grid.dzs[x] for x in path.replace("\n", "")]

z = grid.z("@")
grid[z] = "."
for dz in dzs:
    val = grid[z + dz]
    if val == "#":
        continue
    elif val == ".":
        z += dz
    elif val == "O":
        zs = [z + dz]
        while grid.get(zs[-1] + dz) == "O":
            zs.append(zs[-1] + dz)
        if grid.get(zs[-1] + dz) == "#":
            continue
        zs.append(zs[-1] + dz)
        grid[zs[0]] = "."
        grid.update(dict.fromkeys(zs[1:], "O"))
        z += dz

a = int(sum(z.real + 100*z.imag for z in grid.z("O", first=False)))
print("answer_a:", a)


class Box:
    def __init__(self, z):
        self.z = z

    def __contains__(self, z):
        return z == self.z or z - 1 == self.z

    def can_move(self, dz):
        if dz == -1 and grid[self.z + dz] == "#":
            return False
        if dz == 1 and grid[self.z + 1 + dz] == "#":
            return False
        if dz in (-1j, 1j) and (grid[self.z + dz] == "#" or grid[self.z + 1 + dz] == "#"):
            return False
        if dz == -1:
            for box in boxes:
                if self.z + dz in box:
                    return box.can_move(dz)
            return True
        if dz == 1:
            for box in boxes:
                if self.z + 1 + dz in box:
                    return box.can_move(dz)
            return True
        box2 = [x for x in boxes if self.z + dz in x or self.z + 1 + dz in x]
        return all(b.can_move(dz) for b in box2)

    def move(self, dz):
        if dz == -1:
            for box in boxes:
                if self.z + dz in box:
                    box.move(dz)
        elif dz == 1:
            for box in boxes:
                if self.z + 1 + dz in box:
                    box.move(dz)
        else:
            for box in boxes:
                if self.z + dz in box or self.z + 1 + dz in box:
                    box.move(dz)
        self.z += dz


remap = {
    "#": "##",
    "O": "[]",
    ".": "..",
    "@": "@.",
}
grid = ZGrid(warehouse.translate(str.maketrans(remap)))
boxes = []
for z_, g in grid.items():
    if g == "[":
        boxes.append(Box(z_))
        grid[z_] = "."
    elif g == "]":
        grid[z_] = "."
    elif g == "@":
        z = z_
        grid[z_] = "."

for dz in dzs:
    if grid[z + dz] == "#":
        continue
    box = [x for x in boxes if z + dz in x]
    if box:
        [box] = box
        if not box.can_move(dz):
            continue
        box.move(dz)
    z += dz

b = int(sum(box.z.real + 100*box.z.imag for box in boxes))
print("answer_b:", b)
