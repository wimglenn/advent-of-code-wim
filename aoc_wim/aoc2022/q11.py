"""
--- Day 11: Monkey in the Middle ---
https://adventofcode.com/2022/day/11
"""
from aocd import data
from parse import parse
from collections import deque
from heapq import nlargest
from math import prod


template = """\
Monkey {:d}:
  Starting items: {items}
  Operation: new = {x} {op} {y}
  Test: divisible by {div:d}
    If true: throw to monkey {mt:d}
    If false: throw to monkey {mf:d}"""


class Monkey:

    def __init__(self, items, x, op, y, div, mt, mf):
        self.items = items
        self.x = x
        self.op = op
        self.y = y
        self.div = div
        self.mt = mt
        self.mf = mf
        self.inspected = 0

    @classmethod
    def fromchunk(cls, chunk):
        parsed = parse(template, chunk).named
        items = deque(map(int, parsed.pop("items").split(", ")))
        return cls(items, **parsed)

    def inspect(self):
        while self.items:
            i = self.items.popleft()
            x = i if self.x == "old" else int(self.x)
            y = i if self.y == "old" else int(self.y)
            i = x + y if self.op == "+" else x * y
            i = i // 3 if part == "a" else i % denom
            mnext = self.mf if i % self.div else self.mt
            monkeys[mnext].items.append(i)
            self.inspected += 1


for part, nrounds in zip("ab", (20, 10000)):
    monkeys = [Monkey.fromchunk(x) for x in data.split("\n\n")]
    denom = prod([m.div for m in monkeys])
    for round in range(nrounds):
        for monkey in monkeys:
            monkey.inspect()
    print(f"part {part}:", prod(nlargest(2, [m.inspected for m in monkeys])))
