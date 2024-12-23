"""
--- Day 22: Sand Slabs ---
https://adventofcode.com/2023/day/22
"""
from aocd import data
from dataclasses import dataclass
import operator as op


@dataclass
class Brick:
    x0: int
    y0: int
    z0: int
    x1: int
    y1: int
    z1: int
    id: int = None

    @classmethod
    def fromline(cls, line):
        return cls(*map(int, line.replace("~", ",").split(",")))

    def __post_init__(self):
        if self.x0 > self.x1 or self.y0 > self.y1 or self.z0 > self.z1:
            raise ValueError(f"Invalid brick {self}")

    def cells(self, dz=0):
        xs = range(self.x0, self.x1 + 1)
        ys = range(self.y0, self.y1 + 1)
        zs = range(self.z0, self.z1 + 1)
        return {(x, y, z + dz) for x in xs for y in ys for z in zs}

    def above(self):
        xs = range(self.x0, self.x1 + 1)
        ys = range(self.y0, self.y1 + 1)
        return {(x, y, self.z1 + 1) for x in xs for y in ys}

    def below(self):
        xs = range(self.x0, self.x1 + 1)
        ys = range(self.y0, self.y1 + 1)
        return {(x, y, self.z0 - 1) for x in xs for y in ys}

    def fall(self):
        self.z0 -= 1
        self.z1 -= 1


tdata = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
# data = tdata

bricks = [Brick.fromline(x) for x in data.splitlines()]
bricks.sort(key=op.attrgetter("z0"))
space = {}
for i, brick in enumerate(bricks):
    brick.id = i
    xs = range(brick.x0, brick.x1 + 1)
    ys = range(brick.y0, brick.y1 + 1)
    zs = range(brick.z0, brick.z1 + 1)
    space.update(dict.fromkeys(brick.cells(), brick.id))

while True:
    mutated = False
    for brick in bricks:
        if brick.z0 == 1:
            continue
        if not space.keys() & brick.below():
            for cell in brick.cells():
                del space[cell]
            brick.fall()
            space.update()
            for cell in brick.cells():
                space[cell] = brick.id
            mutated = True
    if not mutated:
        break

bricks_below = [set() for b in bricks]
bricks_above = [set() for b in bricks]
for brick in bricks:
    for cell in brick.above():
        if cell in space:
            bricks_above[brick.id].add(space[cell])
            bricks_below[space[cell]].add(brick.id)

supports = [set() for b in bricks]
for brick in bricks:
    for brick_above in bricks_above[brick.id]:
        if len(bricks_below[brick_above]) == 1:
            supports[brick.id].add(brick_above)

a = sum(not s for s in supports)
print("answer_a:", a)

b = 0
for brick in bricks:
    stack = list(supports[brick.id])
    cumulative_support = set()
    while stack:
        b_id = stack.pop()
        cumulative_support.add(b_id)
        for brick_above in bricks_above[b_id]:
            if bricks_below[brick_above] <= cumulative_support:
                stack.append(brick_above)
    b += len(cumulative_support)
print("answer_b:", b)
